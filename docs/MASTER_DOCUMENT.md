# AMR Characterization in Urban Wastewater: Master Document

## Project Reference Document

**Title**: Medical Waste Influence on AMR Gene Patterns in Tier-2 Indian City Wastewater  
**Degree**: Master's Thesis  
**Last Updated**: 2026-01-28  
**Document Version**: 1.0

> **This is the single authoritative reference document for all analysis, reporting, and future extensions of this project.**

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [One Health Framework](#2-one-health-framework)
3. [Research Questions & Objectives](#3-research-questions--objectives)
4. [Analytical Dimensions](#4-analytical-dimensions)
5. [Spatial Gradient Framework](#5-spatial-gradient-framework)
6. [Tier-2 Inference Logic](#6-tier-2-inference-logic)
7. [Interpretation Boundaries](#7-interpretation-boundaries)
8. [Data Sources & Strategy](#8-data-sources--strategy)
9. [Analytical Methods](#9-analytical-methods)
10. [Technical Infrastructure](#10-technical-infrastructure)
11. [Project Status & Milestones](#11-project-status--milestones)
12. [Change Log](#12-change-log)

---

## 1. Project Overview

This research project characterizes antimicrobial resistance (AMR) gene patterns in urban wastewater systems through secondary analysis of publicly available metagenomic datasets. The study focuses on ecological characterization of resistance patterns within a One Health framework, with particular relevance to Tier-2 Indian urban contexts.

### Core Methodology

- **Secondary Analysis**: Utilization of publicly available metagenomic datasets (FASTQ) from international repositories
- **Comparative Ecology**: Baseline-referenced comparison of resistance patterns across different wastewater contexts
- **Population-Level Focus**: Aggregated ecological signals rather than individual-level or clinical inference
- **Result-Inference Approach**: Deriving actionable ecological insights from metagenomic analysis

---

## 2. One Health Framework

The project is positioned within the **One Health** paradigm, recognizing antimicrobial resistance as an interconnected challenge spanning human, animal, and environmental health domains.

### Wastewater as the Integrative Interface

Urban wastewater serves as a population-level "matrix" that:

- **Aggregates** AMR signals from community households and healthcare facilities
- **Integrates** resistance patterns across the human–animal–environment interface
- **Reflects** collective urban antibiotic pressure rather than individual source attribution
- **Enables** comparative ecological characterization without requiring direct clinical sampling

### Domain Interactions

| Domain            | Contribution to Wastewater Signal                                            |
| ----------------- | ---------------------------------------------------------------------------- |
| **Human Health**  | Community antibiotic use, hospital effluents, metabolized pharmaceuticals    |
| **Animal Health** | Veterinary antibiotic residues, agricultural runoff (where applicable)       |
| **Environmental** | Background environmental resistance, natural attenuation, selection pressure |

---

## 3. Research Questions & Objectives

### Primary Research Question

> How do antibiotic resistance gene (ARG) patterns differ between medical-influenced wastewater and non-medical urban wastewater streams, and what ecological insights can be derived for Tier-2 Indian urban contexts?

### Secondary Questions

1. What is the relative contribution of healthcare facilities to urban wastewater resistome profiles?
2. How do ARG abundance and diversity metrics vary along the upstream–catchment–downstream spatial gradient?
3. Which resistance mechanisms show differential enrichment in medical vs. non-medical streams?

### Objectives

- [x] Establish a reproducible bioinformatics pipeline for ARG annotation and ecological profiling
- [x] Curate publicly available metagenomic datasets representing diverse wastewater contexts
- [ ] Perform comparative resistome analysis using baseline-referenced methodology
- [ ] Generate ecological characterization outputs for Tier-2 urban inference

---

## 4. Analytical Dimensions

The project employs two complementary analytical axes for comprehensive ecological characterization:

### Axis 1: Medical vs. Non-Medical Comparison

| Category               | Definition                                                       | ARG Expectation                                           |
| ---------------------- | ---------------------------------------------------------------- | --------------------------------------------------------- |
| **Medical-Influenced** | Hospital wastewater, healthcare facility effluents               | Elevated clinical ARG signatures, point-source enrichment |
| **Non-Medical**        | Community sewage, urban wastewater without direct hospital input | Baseline community resistance, diffuse inputs             |

### Axis 2: Spatial Gradient (Upstream–Catchment–Downstream)

See [Section 5: Spatial Gradient Framework](#5-spatial-gradient-framework) for detailed definition.

### Complementary Analysis

These two axes are used in combination:

- **Cross-classification**: Samples may be classified on both axes simultaneously
- **Synergistic insight**: Medical influence can be assessed at different spatial positions
- **Data gap mitigation**: Spatial gradient data can supplement limited direct hospital wastewater datasets

---

## 5. Spatial Gradient Framework

An **upstream–catchment–downstream** spatial gradient serves as an explicit analytical dimension for ARG assessment within the One Health wastewater framework.

### Zone Definitions

| Zone           | Definition                                                                                       | Environmental Context                                            | ARG Signal Interpretation                                                                                           |
| -------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Upstream**   | Baseline/background environmental sites located before major urban/industrial discharge points   | Minimal anthropogenic influence, reference water quality         | Environmental baseline ARG signal; minimal urban or clinical influence; reference for comparative analysis          |
| **Catchment**  | Integrative urban zones receiving mixed inputs from residential, commercial, and diffuse sources | Urban core areas, mixed land use, incomplete sewage segregation  | Aggregated signal reflecting mixed residential, commercial, and diffuse healthcare contributions                    |
| **Downstream** | Cumulative urban endpoints located after major urban discharge confluence                        | Post-urban discharge, treatment plant outflows, receiving waters | Amplified urban and medical influence on ARG abundance and resistance mechanisms; cumulative anthropogenic pressure |

### Analytical Purpose

This gradient is used for **comparative ecological interpretation**, not for:

- ❌ Causal inference
- ❌ Transmission tracking
- ❌ Risk prediction
- ❌ Source attribution

**Legitimate applications include:**

1. **Comparative ARG Abundance**: Quantifying relative differences in ARG read counts or normalized abundance across gradient zones
2. **Diversity Pattern Analysis**: Assessing alpha/beta diversity shifts from upstream to downstream
3. **Resistance Mechanism Profiling**: Identifying which ARG classes show spatial enrichment patterns
4. **Environmental Pressure Proxy**: Using gradient position as a proxy for cumulative anthropogenic stressors
5. **Data Gap Mitigation**: Justifying inclusion of river-linked urban wastewater datasets when direct Tier-2 hospital wastewater data are limited

### Gradient-to-Outcome Linkages

| Gradient Position                | Expected ARG Pattern                                 | Ecological Interpretation                               |
| -------------------------------- | ---------------------------------------------------- | ------------------------------------------------------- |
| Upstream → Catchment             | Increasing abundance, diversifying mechanisms        | Urban input accumulation begins                         |
| Catchment → Downstream           | Further enrichment, clinical signature amplification | Cumulative medical and anthropogenic influence          |
| Upstream ↔ Downstream (contrast) | Differential enrichment ratios                       | Magnitude of urban/medical impact on resistance ecology |

---

## 6. Tier-2 Inference Logic

### Definition

Tier-2 urban relevance is defined by **infrastructural characteristics** rather than administrative city labels:

- Mixed land use patterns (residential, commercial, healthcare zones in proximity)
- Incomplete wastewater segregation
- Direct healthcare waste entry into municipal systems
- Limited treatment infrastructure

### Inference Approach

| Aspect                 | Approach                                                                     |
| ---------------------- | ---------------------------------------------------------------------------- |
| **Representation**     | No dataset is presented as a direct representation of a specific Tier-2 city |
| **Analogy**            | Structural and infrastructural analogy enables relevance inference           |
| **Conditionality**     | All Tier-2 inferences are explicitly conditional and comparative             |
| **Baseline Reference** | Tier-1 Indian and international datasets serve as reference baselines        |

### Justification for Dataset Selection

When direct Tier-2 hospital wastewater datasets are limited:

1. **Spatial gradient datasets** (river-linked urban wastewater) provide comparable ecological signals
2. **Infrastructural analogy** justifies extrapolation from structurally similar contexts
3. **Baseline-referenced comparison** maintains methodological rigor

---

## 7. Interpretation Boundaries

To maintain methodological transparency and scientific rigor, the following boundaries are **strictly enforced**:

### What This Study Provides

| ✅ Included                     | Description                                                                      |
| ------------------------------- | -------------------------------------------------------------------------------- |
| **Ecological Characterization** | Population-level patterns of ARG abundance and diversity                         |
| **Comparative Analysis**        | Baseline-referenced differences between sample categories                        |
| **Diversity Metrics**           | Alpha diversity (Shannon, Simpson, Chao1) and beta diversity (Bray-Curtis, PCoA) |
| **Differential Abundance**      | Statistical comparison of ARG enrichment patterns                                |
| **Spatial Contrast**            | Relative ecological pressure across gradient zones                               |

### What This Study Does NOT Provide

| ❌ Excluded                   | Rationale                                                               |
| ----------------------------- | ----------------------------------------------------------------------- |
| **Causal Inference**          | Wastewater metagenomics cannot establish causation                      |
| **Clinical Inference**        | Population-level data cannot inform individual patient outcomes         |
| **Transmission Tracking**     | Metagenomic snapshot data cannot trace resistance transmission pathways |
| **Source Attribution**        | Aggregated signals cannot be decomposed to specific sources             |
| **Risk Prediction**           | Ecological patterns do not translate to quantitative risk assessment    |
| **Individual Identification** | All analysis is de-identified and population-level                      |

### Explicit Constraints

- **Aggregated Signal Only**: Wastewater data reflects collective urban pressure, not individual risk or source-specific causality
- **Spatial Gradient as Contrast**: Upstream–downstream differences indicate relative ecological pressure, not transmission vectors
- **No Direct Tier-2 Representation**: Inferences are analogical, not representative

---

## 8. Data Sources & Strategy

### Data Sourcing Approach

- **Secondary Analysis**: Publicly available metagenomic datasets (FASTQ) from NCBI SRA / ENA / DRA
- **No Primary Sampling**: This study does not involve original sample collection
- **Open Data Priority**: All source data are publicly accessible for reproducibility

### Dataset Categories

#### Category A: Hospital/Healthcare Wastewater (Medical-Influenced)

| BioProject  | Description                                            | Location       | Priority      |
| ----------- | ------------------------------------------------------ | -------------- | ------------- |
| PRJNA682952 | Urban & rural hospital wastewater metagenomics         | Northern India | **Primary**   |
| PRJNA770854 | Eye & general hospital wastewater (pre/post treatment) | Asia           | Supplementary |
| PRJNA947333 | Hospital & community wastewater AMR detection          | Global         | Validation    |
| PRJNA723368 | Untreated hospital wastewater (3 hospitals)            | Global         | Reference     |

#### Category B: Urban/Community Wastewater (Non-Medical Reference)

| BioProject  | Description                      | Location | Purpose            |
| ----------- | -------------------------------- | -------- | ------------------ |
| PRJNA683044 | Conventional WWTP metagenomics   | Global   | Treatment baseline |
| TBD         | Indian urban sewage surveillance | India    | Tier-2 analogy     |

#### Category C: DRA Hospital Wastewater Runs

| Accession Range       | Count | Description                     |
| --------------------- | ----- | ------------------------------- |
| DRR680724 – DRR680775 | 52    | Hospital wastewater metagenomes |

### Dataset Selection Criteria

1. **Sample Type**: Urban wastewater, hospital wastewater, or sewage metagenomes
2. **Geographic Relevance**: Preference for Indian datasets; global datasets for baseline comparisons
3. **Data Type**: Shotgun metagenomic sequencing (WGS), not amplicon-based
4. **Accessibility**: Publicly available with clear metadata
5. **Comparative Potential**: Must enable medical vs. non-medical or gradient-based comparisons

### Master Catalog

- **Primary Reference**: `data/Datasets_Master.xlsx`
- **Registry**: `data/metadata/dataset_registry.md`
- **Sample Manifest**: `data/metadata/sample_manifest.tsv`

---

## 9. Analytical Methods

### Bioinformatics Pipeline

```
Raw FASTQ → Quality Control → Trimming → ARG Annotation → Ecological Profiling
```

| Stage                    | Tool              | Purpose                                  |
| ------------------------ | ----------------- | ---------------------------------------- |
| Quality Assessment       | FastQC            | Sequence quality metrics                 |
| Read Trimming            | fastp             | Adapter removal, quality filtering       |
| ARG Annotation           | RGI (CARD)        | Resistance gene identification           |
| Supplementary Annotation | ResFinder         | Cross-validation                         |
| Taxonomic Context        | Kraken2/MetaPhlAn | Microbial community profiling (optional) |

### Statistical Analysis

#### Alpha Diversity (Within-Sample)

- Shannon Index: Evenness-weighted diversity
- Simpson Index: Dominance-based diversity
- Chao1: Richness estimation
- Pielou Evenness: Distribution uniformity

#### Beta Diversity (Between-Sample)

- Bray-Curtis Dissimilarity: Abundance-weighted distance
- Jaccard Distance: Presence/absence distance
- PCoA/NMDS: Ordination visualization

#### Differential Abundance

- Wilcoxon Rank-Sum: Non-parametric comparison
- FDR Correction: Multiple testing adjustment
- Effect Size: Magnitude of difference estimation

### Output Types

1. **ARG Abundance Tables**: Normalized read counts per sample
2. **Diversity Metrics**: Alpha/beta diversity scores
3. **Differential Enrichment**: Statistical comparison results
4. **Summary Reports**: Aggregated ecological characterization

---

## 10. Technical Infrastructure

### Repository Structure

```
amr-wastewater thesis/
├── data/                    # Metadata and processed results
│   ├── metadata/            # Sample manifests, dataset registries
│   └── processed/           # ARG abundance tables (generated)
├── docs/                    # Documentation (this master document)
├── logs/                    # Decision logs, progress tracking
├── pipeline/                # Bioinformatics and analysis code
│   ├── amr_pipeline.py      # Main bioinformatics pipeline
│   └── ecological_analysis.py # Statistical analysis module
├── visualization/           # Static figures (optional, legacy)
├── requirements.txt         # Python dependencies
└── README.md                # Project entry point
```

### Key Files

| File                                | Purpose                                            |
| ----------------------------------- | -------------------------------------------------- |
| `docs/MASTER_DOCUMENT.md`           | **This document** – Single authoritative reference |
| `pipeline/amr_pipeline.py`          | Bioinformatics workflow scaffolding                |
| `pipeline/ecological_analysis.py`   | Statistical analysis functions                     |
| `data/metadata/dataset_registry.md` | Curated dataset catalog                            |
| `data/Datasets_Master.xlsx`         | Comprehensive dataset annotations                  |
| `requirements.txt`                  | Python package dependencies                        |

### Dependencies

**Python Packages** (see `requirements.txt`):

- Core: numpy, pandas, matplotlib, seaborn
- Bioinformatics: biopython, pysam
- Statistics: scipy, scikit-bio, statsmodels, scikit-learn
- Workflow: snakemake (optional)
- Reporting: multiqc

**External Tools** (conda/system):

- FastQC, fastp, RGI, Kraken2 (optional)

---

## 11. Project Status & Milestones

### Completed ✅

- [x] **Research Framework & Conceptualization**
  - One Health alignment and framing
  - Urban matrix definition
  - Tier-2 inference logic
  - Spatial gradient framework
  - Interpretation boundaries
- [x] **Technical Infrastructure**
  - Bioinformatics pipeline scaffolding
  - Ecological analysis module
  - Project structure and organization
- [x] **Data Strategy**
  - Dataset identification and curation
  - Metadata standards definition
  - Registry and catalog creation

### In Progress 🔄

- [ ] **Metadata Enrichment**: Fetch full metadata for DRA runs using Entrez utilities
- [ ] **Environment Setup**: Configure conda environment with bioinformatics tools
- [ ] **Pilot Analysis**: Run pipeline on subset of samples to validate workflow

### Planned 📋

- [ ] **Full Dataset Processing**: Complete QC and ARG annotation for all samples
- [ ] **Comparative Analysis**: Generate ARG profiles and diversity metrics
- [ ] **Result Synthesis**: Ecological characterization and interpretation
- [ ] **Thesis Writing**: Manuscript preparation

---

## 12. Change Log

| Date           | Version | Changes                                                                                                                                                                  |
| -------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **2026-01-28** | 1.0     | Master document created; integrated upstream–catchment–downstream spatial gradient framework; consolidated all project documentation into single authoritative reference |
| **2026-01-26** | --      | Major infrastructure update: bioinformatics pipeline, ecological analysis module, dataset registry, requirements.txt                                                     |
| **2026-01-25** | --      | Tier-2 inference logic and baseline-referenced interpretation framework established                                                                                      |
| **2026-01-24** | --      | Initial project scaffolding and research framework conceptualization                                                                                                     |

---

## Document Authority

> **This Master Document is the single authoritative reference for:**
>
> - Analysis design and execution
> - Reporting and interpretation
> - Future project extensions
> - Methodological decisions
>
> All other documentation files in this repository are supplementary and should defer to this document in case of conflict.

---

_End of Master Document_
