# Workflow Automation

This folder contains scripts and configuration files for automated workflow execution.

## Files

### Snakefile
- **Purpose:** Snakemake workflow automation
- **Content:** Rules defining the complete data pipeline
- **Workflow Steps:**
  1. Data integration (`integrate_data` rule)
  2. Analysis and visualization (`analyze_and_visualize` rule)
- **Usage:** `snakemake --cores 1`
- **Workflow Step:** Automation - manages dependencies and execution order

### config.yaml
- **Purpose:** Configuration file for workflow
- **Content:** 
  - File paths
  - Analysis parameters
  - Visualization settings
  - Project metadata
- **Workflow Step:** Automation - centralized configuration

### run_all.sh
- **Purpose:** Manual workflow execution script
- **Content:** Bash script to run entire pipeline sequentially
- **Usage:** `./run_all.sh`
- **Workflow Step:** Alternative automation method (for systems without Snakemake)

### workflow_documentation.md
- **Purpose:** Complete workflow guide
- **Content:**
  - Step-by-step execution instructions
  - Prerequisites
  - Troubleshooting guide
  - Expected outputs
- **Workflow Step:** Documentation - reproducibility instructions

### README.md (This file)
- **Purpose:** Workflow folder overview

---

## Workflow Overview

```
Raw Data → Integration → Analysis → Visualization → Results
```

**Automated Execution:**
```bash
snakemake --cores 1
```

**Manual Execution:**
```bash
./run_all.sh
```

---

## What These Files Support

**Reproducibility [20 pts]:**
- Automated workflow ensures consistent execution
- Configuration files document parameters
- Documentation enables independent reproduction

**Transparency [20 pts]:**
- All workflow steps clearly defined
- Execution logs generated automatically
- Complete provenance tracking

---

**Navigation:**
- Project root: `../`
- Scripts: `../scripts/`
- Results: `../results/`
