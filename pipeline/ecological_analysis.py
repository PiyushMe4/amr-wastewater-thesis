"""
AMR Wastewater Thesis - Ecological & Statistical Analysis
==========================================================

Diversity metrics, differential abundance analysis, and statistical comparisons
for ARG profiles between medical-influenced and non-medical wastewater streams.

Author: AMR Thesis Project
Last Updated: 2026-01-26

Analysis Components:
1. Alpha Diversity (Shannon, Simpson, Chao1)
2. Beta Diversity (Bray-Curtis, Jaccard)
3. Differential Abundance (DESeq2-style, Wilcoxon)
4. Visualization Utilities
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import json
import warnings
warnings.filterwarnings('ignore')

# Conditional imports for optional dependencies
try:
    from scipy import stats
    from scipy.spatial.distance import braycurtis, jaccard, pdist, squareform
    from scipy.cluster.hierarchy import linkage, dendrogram
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

try:
    from sklearn.manifold import TSNE
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class SampleMetadata:
    """Metadata for a wastewater sample."""
    sample_id: str
    bioproject: str
    sample_type: str  # 'medical_influenced' or 'non_medical'
    location: str
    country: str
    collection_date: str


@dataclass
class ARGProfile:
    """ARG abundance profile for a sample."""
    sample_id: str
    arg_counts: Dict[str, float]  # ARG name -> normalized abundance
    drug_class_counts: Dict[str, float]
    mechanism_counts: Dict[str, float]
    total_reads: int
    arg_reads: int


# ============================================================================
# ALPHA DIVERSITY METRICS
# ============================================================================

class AlphaDiversity:
    """Calculate within-sample diversity metrics."""
    
    @staticmethod
    def shannon_index(counts: np.ndarray) -> float:
        """
        Calculate Shannon diversity index (H').
        H' = -Σ(pi * ln(pi))
        """
        # Remove zeros and calculate proportions
        counts = np.array(counts, dtype=float)
        counts = counts[counts > 0]
        
        if len(counts) == 0:
            return 0.0
        
        proportions = counts / counts.sum()
        return -np.sum(proportions * np.log(proportions))
    
    @staticmethod
    def simpson_index(counts: np.ndarray) -> float:
        """
        Calculate Simpson diversity index (1 - D).
        D = Σ(ni * (ni - 1)) / (N * (N - 1))
        Returns 1 - D for interpretability (higher = more diverse).
        """
        counts = np.array(counts, dtype=float)
        counts = counts[counts > 0]
        
        if len(counts) == 0:
            return 0.0
        
        n_total = counts.sum()
        if n_total <= 1:
            return 0.0
        
        d = np.sum(counts * (counts - 1)) / (n_total * (n_total - 1))
        return 1 - d
    
    @staticmethod
    def chao1_estimator(counts: np.ndarray) -> float:
        """
        Estimate true richness using Chao1 estimator.
        Chao1 = S_obs + (f1² / 2*f2)
        where f1 = singletons, f2 = doubletons
        """
        counts = np.array(counts, dtype=float)
        counts = counts[counts > 0]
        
        s_obs = len(counts)  # Observed richness
        f1 = np.sum(counts == 1)  # Singletons
        f2 = np.sum(counts == 2)  # Doubletons
        
        if f2 == 0:
            # Bias correction when no doubletons
            return s_obs + (f1 * (f1 - 1)) / 2
        
        return s_obs + (f1 ** 2) / (2 * f2)
    
    @staticmethod
    def observed_richness(counts: np.ndarray) -> int:
        """Count observed ARGs (richness)."""
        counts = np.array(counts, dtype=float)
        return int(np.sum(counts > 0))
    
    @staticmethod
    def pielou_evenness(counts: np.ndarray) -> float:
        """
        Calculate Pielou's evenness (J').
        J' = H' / ln(S)
        """
        shannon = AlphaDiversity.shannon_index(counts)
        richness = AlphaDiversity.observed_richness(counts)
        
        if richness <= 1:
            return 0.0
        
        return shannon / np.log(richness)
    
    def calculate_all(self, counts: np.ndarray) -> Dict[str, float]:
        """Calculate all alpha diversity metrics."""
        return {
            "observed_richness": self.observed_richness(counts),
            "shannon_index": round(self.shannon_index(counts), 4),
            "simpson_index": round(self.simpson_index(counts), 4),
            "chao1_estimator": round(self.chao1_estimator(counts), 4),
            "pielou_evenness": round(self.pielou_evenness(counts), 4)
        }


# ============================================================================
# BETA DIVERSITY METRICS
# ============================================================================

class BetaDiversity:
    """Calculate between-sample diversity and distance metrics."""
    
    def __init__(self):
        if not SCIPY_AVAILABLE:
            raise ImportError("scipy is required for beta diversity calculations")
    
    @staticmethod
    def bray_curtis_distance(sample1: np.ndarray, sample2: np.ndarray) -> float:
        """
        Calculate Bray-Curtis dissimilarity.
        BC = Σ|xi - yi| / Σ(xi + yi)
        """
        sample1 = np.array(sample1, dtype=float)
        sample2 = np.array(sample2, dtype=float)
        
        return braycurtis(sample1, sample2)
    
    @staticmethod
    def jaccard_distance(sample1: np.ndarray, sample2: np.ndarray) -> float:
        """
        Calculate Jaccard distance (presence/absence).
        J = 1 - (|A ∩ B| / |A ∪ B|)
        """
        # Convert to binary (presence/absence)
        s1_binary = (np.array(sample1) > 0).astype(float)
        s2_binary = (np.array(sample2) > 0).astype(float)
        
        return jaccard(s1_binary, s2_binary)
    
    def distance_matrix(self, 
                        abundance_matrix: np.ndarray,
                        sample_ids: List[str],
                        metric: str = "braycurtis") -> pd.DataFrame:
        """
        Calculate pairwise distance matrix.
        
        Args:
            abundance_matrix: Samples x Features matrix
            sample_ids: List of sample identifiers
            metric: Distance metric ('braycurtis', 'jaccard', 'euclidean')
        
        Returns:
            Distance matrix as pandas DataFrame
        """
        distances = pdist(abundance_matrix, metric=metric)
        dist_matrix = squareform(distances)
        
        return pd.DataFrame(
            dist_matrix,
            index=sample_ids,
            columns=sample_ids
        )
    
    def pcoa(self, distance_matrix: pd.DataFrame, 
             n_components: int = 2) -> Tuple[pd.DataFrame, np.ndarray]:
        """
        Perform Principal Coordinates Analysis (PCoA).
        
        Returns:
            coordinates: DataFrame with PC coordinates
            explained_variance: Proportion of variance explained
        """
        # Classical MDS / PCoA implementation
        n = len(distance_matrix)
        dist_sq = np.array(distance_matrix) ** 2
        
        # Double centering
        row_means = dist_sq.mean(axis=1, keepdims=True)
        col_means = dist_sq.mean(axis=0, keepdims=True)
        grand_mean = dist_sq.mean()
        
        B = -0.5 * (dist_sq - row_means - col_means + grand_mean)
        
        # Eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(B)
        
        # Sort by eigenvalue (descending)
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # Select top components
        eigenvalues = eigenvalues[:n_components]
        eigenvectors = eigenvectors[:, :n_components]
        
        # Calculate coordinates
        coordinates = eigenvectors * np.sqrt(np.maximum(eigenvalues, 0))
        
        # Explained variance
        total_variance = np.sum(np.maximum(eigenvalues, 0))
        explained_variance = eigenvalues / total_variance if total_variance > 0 else eigenvalues
        
        coord_df = pd.DataFrame(
            coordinates,
            index=distance_matrix.index,
            columns=[f"PC{i+1}" for i in range(n_components)]
        )
        
        return coord_df, explained_variance


# ============================================================================
# DIFFERENTIAL ABUNDANCE ANALYSIS
# ============================================================================

class DifferentialAbundance:
    """Statistical tests for differential ARG abundance."""
    
    def __init__(self):
        if not SCIPY_AVAILABLE:
            raise ImportError("scipy is required for statistical tests")
    
    @staticmethod
    def wilcoxon_rank_sum(group1: np.ndarray, 
                          group2: np.ndarray) -> Tuple[float, float]:
        """
        Perform Wilcoxon rank-sum test (Mann-Whitney U).
        Non-parametric comparison of two groups.
        
        Returns:
            statistic: U statistic
            p_value: Two-sided p-value
        """
        statistic, p_value = stats.mannwhitneyu(
            group1, group2, 
            alternative='two-sided'
        )
        return statistic, p_value
    
    @staticmethod
    def log2_fold_change(group1_mean: float, 
                         group2_mean: float,
                         pseudocount: float = 1.0) -> float:
        """
        Calculate log2 fold change between groups.
        log2FC = log2((group2 + pseudo) / (group1 + pseudo))
        """
        return np.log2((group2_mean + pseudocount) / (group1_mean + pseudocount))
    
    def compare_groups(self,
                       abundance_df: pd.DataFrame,
                       group_labels: pd.Series,
                       group1_name: str = "non_medical",
                       group2_name: str = "medical_influenced") -> pd.DataFrame:
        """
        Compare ARG abundances between two groups.
        
        Args:
            abundance_df: Features x Samples abundance matrix
            group_labels: Series mapping sample IDs to group labels
            group1_name: Reference group name
            group2_name: Comparison group name
        
        Returns:
            DataFrame with differential abundance results
        """
        results = []
        
        group1_samples = group_labels[group_labels == group1_name].index
        group2_samples = group_labels[group_labels == group2_name].index
        
        for feature in abundance_df.index:
            group1_values = abundance_df.loc[feature, group1_samples].values
            group2_values = abundance_df.loc[feature, group2_samples].values
            
            # Skip if both groups have zero values
            if group1_values.sum() == 0 and group2_values.sum() == 0:
                continue
            
            # Statistical test
            stat, p_value = self.wilcoxon_rank_sum(group1_values, group2_values)
            
            # Effect size
            log2fc = self.log2_fold_change(
                group1_values.mean(),
                group2_values.mean()
            )
            
            results.append({
                "feature": feature,
                "mean_group1": group1_values.mean(),
                "mean_group2": group2_values.mean(),
                "log2_fold_change": round(log2fc, 4),
                "statistic": stat,
                "p_value": p_value
            })
        
        result_df = pd.DataFrame(results)
        
        # Multiple testing correction (Benjamini-Hochberg)
        if len(result_df) > 0:
            result_df = self.fdr_correction(result_df)
        
        return result_df.sort_values("p_adjusted")
    
    @staticmethod
    def fdr_correction(result_df: pd.DataFrame, 
                       alpha: float = 0.05) -> pd.DataFrame:
        """Apply Benjamini-Hochberg FDR correction."""
        n = len(result_df)
        result_df = result_df.sort_values("p_value").reset_index(drop=True)
        
        # BH adjustment
        result_df["p_adjusted"] = (
            result_df["p_value"] * n / (result_df.index + 1)
        ).clip(upper=1.0)
        
        # Ensure monotonicity
        result_df["p_adjusted"] = result_df["p_adjusted"][::-1].cummin()[::-1]
        
        # Significance flag
        result_df["significant"] = result_df["p_adjusted"] < alpha
        
        return result_df


# ============================================================================
# ABUNDANCE TABLE UTILITIES
# ============================================================================

class AbundanceTable:
    """Utilities for working with ARG abundance tables."""
    
    @staticmethod
    def normalize_by_total_reads(counts_df: pd.DataFrame,
                                  total_reads: Dict[str, int],
                                  scale: float = 1e6) -> pd.DataFrame:
        """
        Normalize counts to reads per million (RPM).
        RPM = (raw_count / total_reads) * 1e6
        """
        normalized = counts_df.copy()
        
        for sample in normalized.columns:
            if sample in total_reads:
                normalized[sample] = (
                    normalized[sample] / total_reads[sample] * scale
                )
        
        return normalized
    
    @staticmethod
    def aggregate_by_drug_class(arg_df: pd.DataFrame,
                                 arg_to_class: Dict[str, str]) -> pd.DataFrame:
        """Aggregate ARG abundance by antibiotic drug class."""
        arg_df = arg_df.copy()
        arg_df["drug_class"] = arg_df.index.map(arg_to_class).fillna("Unknown")
        
        return arg_df.groupby("drug_class").sum()
    
    @staticmethod
    def filter_low_abundance(abundance_df: pd.DataFrame,
                              min_prevalence: float = 0.1,
                              min_abundance: float = 1.0) -> pd.DataFrame:
        """
        Filter features with low prevalence or abundance.
        
        Args:
            abundance_df: Features x Samples matrix
            min_prevalence: Minimum fraction of samples with presence
            min_abundance: Minimum mean abundance across samples
        """
        # Prevalence filter
        prevalence = (abundance_df > 0).sum(axis=1) / abundance_df.shape[1]
        prevalence_mask = prevalence >= min_prevalence
        
        # Abundance filter
        abundance_mask = abundance_df.mean(axis=1) >= min_abundance
        
        return abundance_df.loc[prevalence_mask & abundance_mask]


# ============================================================================
# MAIN ANALYSIS CLASS
# ============================================================================

class EcologicalAnalysis:
    """Main class for ecological and statistical analysis of ARG data."""
    
    def __init__(self, output_dir: Path = Path("data/analysis_results")):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.alpha = AlphaDiversity()
        self.beta = BetaDiversity() if SCIPY_AVAILABLE else None
        self.diff_abundance = DifferentialAbundance() if SCIPY_AVAILABLE else None
        self.table_utils = AbundanceTable()
    
    def run_full_analysis(self,
                          abundance_file: Path,
                          metadata_file: Path) -> Dict:
        """
        Run complete ecological analysis pipeline.
        
        Args:
            abundance_file: Path to ARG abundance table (TSV/CSV)
            metadata_file: Path to sample metadata (TSV/CSV)
        
        Returns:
            Dictionary with all analysis results
        """
        print("=" * 60)
        print("ECOLOGICAL ANALYSIS - AMR WASTEWATER THESIS")
        print("=" * 60)
        
        # Load data
        print("\n[1/5] Loading data...")
        abundance_df = pd.read_csv(abundance_file, sep='\t', index_col=0)
        metadata_df = pd.read_csv(metadata_file, sep='\t', index_col=0)
        
        results = {
            "samples_analyzed": len(abundance_df.columns),
            "features_analyzed": len(abundance_df.index)
        }
        
        # Alpha diversity
        print("[2/5] Calculating alpha diversity...")
        alpha_results = {}
        for sample in abundance_df.columns:
            counts = abundance_df[sample].values
            alpha_results[sample] = self.alpha.calculate_all(counts)
        
        results["alpha_diversity"] = alpha_results
        
        # Beta diversity
        if self.beta:
            print("[3/5] Calculating beta diversity...")
            dist_matrix = self.beta.distance_matrix(
                abundance_df.T.values,
                list(abundance_df.columns),
                metric="braycurtis"
            )
            pcoa_coords, explained_var = self.beta.pcoa(dist_matrix)
            
            results["beta_diversity"] = {
                "distance_matrix": dist_matrix.to_dict(),
                "pcoa_coordinates": pcoa_coords.to_dict(),
                "explained_variance": explained_var.tolist()
            }
        
        # Differential abundance
        if self.diff_abundance and "sample_type" in metadata_df.columns:
            print("[4/5] Differential abundance analysis...")
            group_labels = metadata_df["sample_type"]
            diff_results = self.diff_abundance.compare_groups(
                abundance_df,
                group_labels
            )
            results["differential_abundance"] = diff_results.to_dict(orient="records")
        
        # Save results
        print("[5/5] Saving results...")
        output_file = self.output_dir / "ecological_analysis_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n✓ Analysis complete. Results saved to: {output_file}")
        
        return results


# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Demo the ecological analysis module."""
    print("AMR Wastewater Thesis - Ecological Analysis Module")
    print("=" * 50)
    print("\nThis module provides:")
    print("  • Alpha diversity (Shannon, Simpson, Chao1)")
    print("  • Beta diversity (Bray-Curtis, PCoA)")
    print("  • Differential abundance (Wilcoxon, FDR correction)")
    print("\nUsage:")
    print("  from ecological_analysis import EcologicalAnalysis")
    print("  analyzer = EcologicalAnalysis()")
    print("  results = analyzer.run_full_analysis(abundance_file, metadata_file)")
    
    # Demo with synthetic data
    print("\n--- Demo with synthetic data ---")
    demo_counts = np.array([100, 50, 30, 20, 10, 5, 3, 2, 1, 1])
    
    alpha = AlphaDiversity()
    demo_results = alpha.calculate_all(demo_counts)
    
    print(f"\nSample diversity metrics:")
    for metric, value in demo_results.items():
        print(f"  {metric}: {value}")


if __name__ == "__main__":
    main()
