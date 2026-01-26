# Implementation Log: AMR Wastewater Thesis

## Overview

This document serves as a living record of the procedures, methodologies, and technical milestones incorporated into the research project: _"Medical Waste Influence on AMR Gene Patterns in Tier-2 Indian City Wastewater"_.

**Last Updated:** 2026-01-26

---

## 1. Research Framework & Conceptualization

- [x] **One Health Alignment**: Established the project within the One Health framework, linking human, animal, and environmental health through the wastewater interface.
- [x] **Urban Matrix Definition**: Defined urban wastewater as a population-level "matrix" that aggregates AMR signals from community households and healthcare facilities.
- [x] **Geographic Focus**: Defined the scope for Tier-2 Indian cities, emphasizing the unique challenges of incomplete waste segregation and mixed land use.
- [x] **Comparative Research Logic**: Established the core methodology of comparing _Medical-influenced_ vs. _Non-medical_ wastewater streams to isolate clinical signatures.
- [x] **Tier-2 Inference Framework**: Defined relevance through structural and infrastructural analogy rather than direct representation, using reference baselines for contextualization.

## 2. Technical Infrastructure & Visualization

- [x] **Automated Figure Generation**: Developed a Python-based pipeline (`visualization/amr_thesis_visualization.py`) using Matplotlib for consistent, publication-grade academic figures.
- [x] **Visual Framework Repository**: Generated and archived five core conceptual figures, labeled as conceptual frameworks with baseline-referenced comparative logic.
- [x] **Interpretation Guardrails**: Explicitly documented boundaries (population-level, no causal/clinical inference) within both documentation and figure annotations.
- [x] **Project Scaffolding**: Structured the repository into functional modules (`data/`, `docs/`, `logs/`, `visualization/`, `pipeline/`).

## 3. Data & Metadata Strategy

- [x] **Data Sourcing Plan**: Defined a secondary analysis strategy using publicly available metagenomic datasets (FASTQ) rather than primary sampling.
- [x] **Metadata Standards**: Established a plan for tracking accessions and sample metadata in the `data/` directory.
- [x] **Dataset Registry**: Created comprehensive dataset registry (`data/metadata/dataset_registry.md`) with curated BioProject accessions.
- [x] **Master Dataset Catalog**: Added `Datasets_Master.xlsx` with annotated dataset information.
- [x] **Hospital Wastewater Runs**: Collected 52 DRA accessions for hospital wastewater samples (`data/hospital_wastewater_runs.txt`).

## 4. Analytical Procedures (Planned/In-Progress)

- [x] **Data Acquisition**: Identified relevant datasets from NCBI SRA/ENA and DRA.
  - PRJNA682952 (Northern India hospital wastewater)
  - PRJNA770854, PRJNA947333, PRJNA723368 (hospital comparisons)
  - 52 DRA hospital wastewater runs (DRR680724-DRR680775)
- [x] **QC Pipeline**: Implemented pipeline scaffolding (`pipeline/amr_pipeline.py`) with FastQC and fastp integration.
- [x] **ARG Annotation**: Integrated CARD/RGI framework in pipeline for ARG detection.
- [x] **Ecological Profiling**: Developed statistical analysis module (`pipeline/ecological_analysis.py`) with:
  - Alpha diversity (Shannon, Simpson, Chao1, Pielou evenness)
  - Beta diversity (Bray-Curtis, Jaccard, PCoA)
  - Differential abundance testing (Wilcoxon, FDR correction)

## 5. Next Steps

- [ ] **Metadata Enrichment**: Fetch full metadata for DRA runs using Entrez utilities
- [ ] **Environment Setup**: Configure conda environment with bioinformatics tools
- [ ] **Pilot Analysis**: Run pipeline on subset of samples to validate workflow
- [ ] **Comparative Visualization**: Generate ARG heatmaps and diversity plots

---

## Change Log

- **2026-01-26**: Major infrastructure update:
  - Added bioinformatics pipeline (`pipeline/amr_pipeline.py`)
  - Added ecological analysis module (`pipeline/ecological_analysis.py`)
  - Created dataset registry and sample manifest
  - Incorporated user-provided Datasets_Master.xlsx and hospital wastewater runs
  - Added requirements.txt for Python dependencies
- **2026-01-25**: Incorporated Tier-2 inference logic and baseline-referenced interpretation framework. Updated documentation and visualization code to reflect interpretation boundaries (population-level, no causal inference).
- **2026-01-24**: Initial creation of the Implementation Log. Consolidated research framework and visualization milestones.
