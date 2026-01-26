"""
AMR Wastewater Thesis - Bioinformatics Pipeline
================================================

Quality control, preprocessing, and ARG annotation pipeline for metagenomic data.

Author: AMR Thesis Project
Last Updated: 2026-01-26

Pipeline Components:
1. Quality Control (FastQC)
2. Read Trimming (Trimmomatic / fastp)
3. Host Read Removal (optional)
4. ARG Annotation (CARD/RGI, ResFinder)
5. Abundance Quantification
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Tuple
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class PipelineConfig:
    """Configuration for the AMR analysis pipeline."""
    
    # Directory structure
    raw_reads_dir: Path = Path("data/raw_reads")
    trimmed_reads_dir: Path = Path("data/trimmed_reads")
    qc_reports_dir: Path = Path("data/qc_reports")
    arg_results_dir: Path = Path("data/arg_annotation")
    logs_dir: Path = Path("logs/pipeline")
    
    # Tool parameters
    threads: int = 4
    min_read_length: int = 50
    min_quality: int = 20
    
    # Database paths (to be configured per system)
    card_db_path: Optional[Path] = None
    resfinder_db_path: Optional[Path] = None
    
    def create_directories(self):
        """Create all required directories."""
        for dir_path in [
            self.raw_reads_dir,
            self.trimmed_reads_dir,
            self.qc_reports_dir,
            self.arg_results_dir,
            self.logs_dir
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(log_file: Path) -> logging.Logger:
    """Configure logging for pipeline execution."""
    logger = logging.getLogger("amr_pipeline")
    logger.setLevel(logging.INFO)
    
    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def check_tool_availability(tool_name: str) -> bool:
    """Check if a command-line tool is available."""
    try:
        subprocess.run(
            [tool_name, "--version"],
            capture_output=True,
            check=False
        )
        return True
    except FileNotFoundError:
        return False


def run_command(cmd: List[str], logger: logging.Logger, 
                description: str = "") -> Tuple[int, str, str]:
    """Execute a shell command and log output."""
    logger.info(f"Running: {description or ' '.join(cmd[:3])}...")
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        logger.error(f"Command failed: {result.stderr}")
    else:
        logger.info(f"Completed: {description}")
    
    return result.returncode, result.stdout, result.stderr


# ============================================================================
# PIPELINE STEPS
# ============================================================================

class QualityControl:
    """Quality control using FastQC."""
    
    def __init__(self, config: PipelineConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
    
    def run_fastqc(self, input_file: Path, output_dir: Optional[Path] = None) -> bool:
        """Run FastQC on a single file."""
        if not check_tool_availability("fastqc"):
            self.logger.warning("FastQC not found. Skipping QC step.")
            return False
        
        output_dir = output_dir or self.config.qc_reports_dir
        
        cmd = [
            "fastqc",
            str(input_file),
            "-o", str(output_dir),
            "-t", str(self.config.threads),
            "--quiet"
        ]
        
        returncode, _, _ = run_command(
            cmd, self.logger, 
            f"FastQC on {input_file.name}"
        )
        
        return returncode == 0
    
    def run_multiqc(self, input_dir: Path, output_dir: Optional[Path] = None) -> bool:
        """Aggregate QC reports with MultiQC."""
        if not check_tool_availability("multiqc"):
            self.logger.warning("MultiQC not found. Skipping aggregation.")
            return False
        
        output_dir = output_dir or self.config.qc_reports_dir
        
        cmd = [
            "multiqc",
            str(input_dir),
            "-o", str(output_dir),
            "-f"  # Force overwrite
        ]
        
        returncode, _, _ = run_command(
            cmd, self.logger,
            "MultiQC aggregation"
        )
        
        return returncode == 0


class ReadTrimming:
    """Read trimming and quality filtering."""
    
    def __init__(self, config: PipelineConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
    
    def run_fastp(self, 
                  input_r1: Path, 
                  input_r2: Optional[Path] = None,
                  output_prefix: Optional[str] = None) -> bool:
        """Run fastp for quality trimming."""
        if not check_tool_availability("fastp"):
            self.logger.warning("fastp not found. Skipping trimming step.")
            return False
        
        output_prefix = output_prefix or input_r1.stem.replace("_1", "").replace("_R1", "")
        output_dir = self.config.trimmed_reads_dir
        
        cmd = [
            "fastp",
            "-i", str(input_r1),
            "-o", str(output_dir / f"{output_prefix}_trimmed_R1.fastq.gz"),
            "-q", str(self.config.min_quality),
            "-l", str(self.config.min_read_length),
            "-w", str(self.config.threads),
            "-j", str(output_dir / f"{output_prefix}_fastp.json"),
            "-h", str(output_dir / f"{output_prefix}_fastp.html")
        ]
        
        # Add paired-end options if R2 exists
        if input_r2 and input_r2.exists():
            cmd.extend([
                "-I", str(input_r2),
                "-O", str(output_dir / f"{output_prefix}_trimmed_R2.fastq.gz")
            ])
        
        returncode, _, _ = run_command(
            cmd, self.logger,
            f"fastp trimming for {output_prefix}"
        )
        
        return returncode == 0


class ARGAnnotation:
    """Antibiotic Resistance Gene annotation using CARD/RGI."""
    
    def __init__(self, config: PipelineConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
    
    def run_rgi_bwt(self, 
                    input_r1: Path, 
                    input_r2: Optional[Path] = None,
                    output_prefix: Optional[str] = None) -> bool:
        """
        Run RGI (Resistance Gene Identifier) for metagenomic ARG detection.
        Uses BWT alignment mode for short reads.
        """
        if not check_tool_availability("rgi"):
            self.logger.warning("RGI not found. Skipping ARG annotation.")
            return False
        
        output_prefix = output_prefix or input_r1.stem.replace("_trimmed_R1", "")
        output_file = self.config.arg_results_dir / output_prefix
        
        cmd = [
            "rgi", "bwt",
            "-1", str(input_r1),
            "-o", str(output_file),
            "-n", str(self.config.threads),
            "--clean"
        ]
        
        # Add paired-end read
        if input_r2 and input_r2.exists():
            cmd.extend(["-2", str(input_r2)])
        
        returncode, _, _ = run_command(
            cmd, self.logger,
            f"RGI BWT annotation for {output_prefix}"
        )
        
        return returncode == 0
    
    def parse_rgi_results(self, result_file: Path) -> dict:
        """Parse RGI output into a structured format."""
        results = {
            "sample": result_file.stem,
            "arg_counts": {},
            "drug_classes": {},
            "mechanisms": {}
        }
        
        # RGI BWT outputs tab-separated files
        gene_mapping_file = result_file.with_suffix(".gene_mapping_data.txt")
        
        if not gene_mapping_file.exists():
            self.logger.warning(f"RGI output not found: {gene_mapping_file}")
            return results
        
        try:
            with open(gene_mapping_file, 'r') as f:
                # Skip header
                next(f, None)
                for line in f:
                    fields = line.strip().split('\t')
                    if len(fields) >= 10:
                        aro_term = fields[0]
                        drug_class = fields[6] if len(fields) > 6 else "Unknown"
                        mechanism = fields[7] if len(fields) > 7 else "Unknown"
                        
                        # Count ARGs
                        results["arg_counts"][aro_term] = results["arg_counts"].get(aro_term, 0) + 1
                        results["drug_classes"][drug_class] = results["drug_classes"].get(drug_class, 0) + 1
                        results["mechanisms"][mechanism] = results["mechanisms"].get(mechanism, 0) + 1
        
        except Exception as e:
            self.logger.error(f"Error parsing RGI results: {e}")
        
        return results


# ============================================================================
# MAIN PIPELINE ORCHESTRATION
# ============================================================================

class AMRPipeline:
    """Main pipeline orchestrator."""
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.config.create_directories()
        
        log_file = config.logs_dir / "pipeline_run.log"
        self.logger = setup_logging(log_file)
        
        # Initialize components
        self.qc = QualityControl(config, self.logger)
        self.trimmer = ReadTrimming(config, self.logger)
        self.annotator = ARGAnnotation(config, self.logger)
    
    def check_dependencies(self) -> dict:
        """Check availability of required tools."""
        tools = ["fastqc", "multiqc", "fastp", "rgi"]
        status = {}
        
        self.logger.info("Checking tool dependencies...")
        for tool in tools:
            available = check_tool_availability(tool)
            status[tool] = available
            self.logger.info(f"  {tool}: {'✓ Available' if available else '✗ Not found'}")
        
        return status
    
    def process_sample(self, 
                       sample_id: str,
                       r1_path: Path,
                       r2_path: Optional[Path] = None) -> dict:
        """Run full pipeline on a single sample."""
        self.logger.info(f"=" * 60)
        self.logger.info(f"Processing sample: {sample_id}")
        self.logger.info(f"=" * 60)
        
        results = {
            "sample_id": sample_id,
            "qc_passed": False,
            "trimming_passed": False,
            "annotation_passed": False,
            "arg_results": None
        }
        
        # Step 1: Initial QC
        self.logger.info("Step 1: Quality Control")
        results["qc_passed"] = self.qc.run_fastqc(r1_path)
        if r2_path:
            self.qc.run_fastqc(r2_path)
        
        # Step 2: Trimming
        self.logger.info("Step 2: Read Trimming")
        results["trimming_passed"] = self.trimmer.run_fastp(r1_path, r2_path, sample_id)
        
        # Step 3: ARG Annotation
        self.logger.info("Step 3: ARG Annotation")
        trimmed_r1 = self.config.trimmed_reads_dir / f"{sample_id}_trimmed_R1.fastq.gz"
        trimmed_r2 = self.config.trimmed_reads_dir / f"{sample_id}_trimmed_R2.fastq.gz"
        
        if trimmed_r1.exists():
            results["annotation_passed"] = self.annotator.run_rgi_bwt(
                trimmed_r1, 
                trimmed_r2 if trimmed_r2.exists() else None,
                sample_id
            )
            
            # Parse results
            result_file = self.config.arg_results_dir / sample_id
            results["arg_results"] = self.annotator.parse_rgi_results(result_file)
        
        self.logger.info(f"Sample {sample_id} processing complete.")
        return results
    
    def process_batch(self, manifest_file: Path) -> List[dict]:
        """Process multiple samples from a manifest file."""
        all_results = []
        
        self.logger.info(f"Loading samples from manifest: {manifest_file}")
        
        # Simple TSV parsing (header: accession, bioproject, ...)
        try:
            with open(manifest_file, 'r') as f:
                header = f.readline().strip().split('\t')
                accession_idx = header.index('accession')
                
                for line in f:
                    fields = line.strip().split('\t')
                    if len(fields) > accession_idx:
                        accession = fields[accession_idx]
                        
                        # Look for read files
                        r1 = self.config.raw_reads_dir / f"{accession}_1.fastq.gz"
                        r2 = self.config.raw_reads_dir / f"{accession}_2.fastq.gz"
                        
                        if r1.exists():
                            result = self.process_sample(
                                accession, r1, 
                                r2 if r2.exists() else None
                            )
                            all_results.append(result)
                        else:
                            self.logger.warning(f"Read files not found for {accession}")
        
        except Exception as e:
            self.logger.error(f"Error processing manifest: {e}")
        
        # Generate summary
        self.generate_summary(all_results)
        
        return all_results
    
    def generate_summary(self, results: List[dict]):
        """Generate pipeline execution summary."""
        summary_file = self.config.arg_results_dir / "pipeline_summary.json"
        
        summary = {
            "total_samples": len(results),
            "qc_passed": sum(1 for r in results if r["qc_passed"]),
            "trimming_passed": sum(1 for r in results if r["trimming_passed"]),
            "annotation_passed": sum(1 for r in results if r["annotation_passed"]),
            "samples": results
        }
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.logger.info(f"Summary saved to: {summary_file}")


# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the pipeline."""
    print("=" * 60)
    print("AMR WASTEWATER THESIS - BIOINFORMATICS PIPELINE")
    print("=" * 60)
    
    # Initialize pipeline
    config = PipelineConfig()
    pipeline = AMRPipeline(config)
    
    # Check dependencies
    print("\nChecking dependencies...")
    dep_status = pipeline.check_dependencies()
    
    missing_tools = [t for t, available in dep_status.items() if not available]
    if missing_tools:
        print(f"\n⚠ Missing tools: {', '.join(missing_tools)}")
        print("Install required tools before running the pipeline.")
        print("\nInstallation suggestions:")
        print("  - FastQC: conda install -c bioconda fastqc")
        print("  - MultiQC: pip install multiqc")
        print("  - fastp: conda install -c bioconda fastp")
        print("  - RGI: conda install -c bioconda rgi")
    else:
        print("\n✓ All dependencies satisfied.")
    
    print("\nPipeline ready. Use process_sample() or process_batch() to run.")
    print("\nExample usage:")
    print("  pipeline.process_sample('SRR13227002', Path('data/raw_reads/SRR13227002_1.fastq.gz'))")
    
    return pipeline


if __name__ == "__main__":
    main()
