# Dataset Registry: AMR Wastewater Thesis

# ==============================================

## Overview

This document catalogs publicly available metagenomic datasets identified for secondary analysis in the thesis:
**"Medical Waste Influence on AMR Gene Patterns in Tier-2 Indian City Wastewater"**

All datasets are sourced from NCBI Sequence Read Archive (SRA) / European Nucleotide Archive (ENA).

---

## Dataset Selection Criteria

1. **Sample Type**: Urban wastewater, hospital wastewater, or sewage metagenomes
2. **Geographic Relevance**: Preference for Indian datasets; global urban datasets for baseline comparisons
3. **Data Type**: Shotgun metagenomic sequencing (WGS), not amplicon-based
4. **Accessibility**: Publicly available with clear metadata
5. **Comparative Potential**: Must enable medical vs. non-medical stream comparisons

---

## Curated Datasets

### Category A: Hospital/Healthcare Wastewater (Medical-Influenced)

| BioProject  | Description                                            | Location       | SRA Accessions                                   | Notes                                        |
| ----------- | ------------------------------------------------------ | -------------- | ------------------------------------------------ | -------------------------------------------- |
| PRJNA682952 | Urban & rural hospital wastewater metagenomics         | Northern India | SRR13227002-SRR13227005, SRR15384559-SRR15384560 | **Primary dataset** - Direct India relevance |
| PRJNA770854 | Eye & general hospital wastewater (pre/post treatment) | Asia           | TBD                                              | Treatment effect comparisons                 |
| PRJNA947333 | Hospital & community wastewater AMR detection          | Global         | TBD                                              | Hospital-community comparison                |
| PRJNA723368 | Untreated hospital wastewater (3 hospitals)            | Global         | TBD                                              | Baseline clinical signatures                 |

### Category B: Urban/Community Wastewater (Non-Medical Reference)

| BioProject  | Description                      | Location | SRA Accessions | Notes                           |
| ----------- | -------------------------------- | -------- | -------------- | ------------------------------- |
| PRJNA683044 | Conventional WWTP metagenomics   | Global   | TBD            | Treatment plant baseline        |
| TBD         | Indian urban sewage surveillance | India    | TBD            | To be identified via SRA search |

### Category C: DRA Hospital Wastewater Runs (52 samples)

**Source File**: `data/hospital_wastewater_runs.txt`

| Accession Range       | Count | Description                     | Notes                           |
| --------------------- | ----- | ------------------------------- | ------------------------------- |
| DRR680724 - DRR680775 | 52    | Hospital wastewater metagenomes | Wastewater surveillance dataset |

### Master Dataset Catalog

**File**: `data/Datasets_Master.xlsx`

This Excel file contains the comprehensive catalog of all datasets under consideration, with annotations for study design, relevance, and prioritization.

---

## Data Acquisition Workflow

### Step 1: Metadata Harvest

```bash
# Use NCBI Entrez utilities to fetch sample metadata
esearch -db sra -query "PRJNA682952" | efetch -format runinfo > PRJNA682952_runinfo.csv
```

### Step 2: Quality Assessment (Pre-Download)

- Review run sizes and sequencing platform consistency
- Verify paired-end vs single-end reads
- Check for sufficient depth (>1M reads preferred)

### Step 3: Selective Download

```bash
# Use fasterq-dump for efficient download
fasterq-dump --split-files SRR13227002 -O raw_reads/
```

### Step 4: Metadata Standardization

Store harmonized metadata in `data/metadata/sample_manifest.tsv` with columns:

- `accession`, `bioproject`, `sample_type`, `location`, `collection_date`, `study_category`

---

## Priority Order for Analysis

1. **PRJNA682952** - Northern India hospital wastewater (primary)
2. **PRJNA947333** - Hospital-community comparative (validation)
3. **PRJNA770854** - Treatment effect analysis (supplementary)

---

## Notes & Considerations

- **Tier-2 Inference**: While datasets may not directly represent Tier-2 cities, structural analogy logic applies (see `docs/IMPLEMENTATION_LOG.md`).
- **Population-Level Only**: All interpretations remain at aggregate, ecological levels—no individual clinical inference.
- **Baseline Referencing**: Non-medical streams serve as ecological baselines, not controls in the experimental sense.

---

## References

1. NCBI SRA: https://www.ncbi.nlm.nih.gov/sra
2. ENA Browser: https://www.ebi.ac.uk/ena/browser/
3. CARD Database: https://card.mcmaster.ca/
4. ResFinder: https://cge.food.dtu.dk/services/ResFinder/

---

**Last Updated:** 2026-01-26
