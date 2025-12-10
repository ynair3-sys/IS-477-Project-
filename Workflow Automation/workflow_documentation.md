# Workflow Documentation

**Project:** Sleep Patterns and Academic Performance Study  
**Last Updated:** December 2025

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Workflow Steps](#workflow-steps)
4. [Automated Execution](#automated-execution)
5. [Manual Execution](#manual-execution)
6. [Outputs](#outputs)
7. [Troubleshooting](#troubleshooting)

---

## Overview

This document describes the complete data analysis workflow for investigating how sleep patterns influence GPA and study productivity among college students.

**Workflow Stages:**
```
Raw Data → Cleaning → Integration → Analysis → Visualization → Results
```

**Total Execution Time:** ~5-10 minutes (depending on system)

---

## Prerequisites

### Software Requirements

1. **Python 3.9+**
   ```bash
   python --version  # Should show 3.9 or higher
   ```

2. **Required Python Packages**
   ```bash
   pip install pandas numpy matplotlib seaborn scipy scikit-learn
   ```
   
   Or install from requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

3. **Optional: Snakemake** (for automated workflow)
   ```bash
   pip install snakemake
   ```

### Data Requirements

You need these cleaned datasets in your project root:
- `cleaned_cmu-sleep.csv` (547 students from CMU dataset)
- `cleaned_student_habits.csv` (1,000 students from Kaggle dataset)

**Note:** If you don't have these, you need to complete the data cleaning step first using OpenRefine.

---

## Workflow Steps

### Step 1: Data Acquisition

**Manual Method:**
```bash
# CMU dataset (automated download)
curl -o cmu-sleep.csv https://cmustatistics.github.io/data-repository/data/cmu-sleep.csv

# Kaggle dataset (requires manual download or Kaggle API)
# Download from: https://www.kaggle.com/datasets/jayaantanaath/student-habits-vs-academic-performance
```

**What happens:**
- Downloads raw datasets
- Verifies file integrity
- Saves to project root

### Step 2: Data Cleaning

**Tool:** OpenRefine (manual step - required for project)

**Input:**
- `cmu-sleep.csv` (raw)
- `student_habits_performance.csv` (raw)

**Output:**
- `cleaned_cmu-sleep.csv` (cleaned)
- `cleaned_student_habits.csv` (cleaned)
- `openrefine_recipe.json` (operation history)

**Cleaning Operations:**
- Remove duplicates
- Handle missing values
- Standardize variable formats
- Fix inconsistencies
- Export JSON recipe for reproducibility

**⚠️ Important:** Save your OpenRefine operation history to `docs/openrefine_recipe.json`

### Step 3: Data Integration

**Script:** `03_data_integration.py`

**Input:**
- `cleaned_cmu-sleep.csv`
- `cleaned_student_habits.csv`

**Output:**
- `data/integrated_data.csv` (1,547 students)

**What it does:**
1. Loads cleaned datasets
2. Standardizes variables:
   - Sleep: CMU minutes → hours
   - GPA: CMU 0-4 scale → 0-100 scale
   - Gender: CMU 0/1 → Male/Female
3. Creates derived variables:
   - Sleep categories (Poor/Insufficient/Adequate/Optimal)
   - Productivity score (Kaggle only)
4. Combines datasets vertically
5. Adds source identifiers (CMU_xxx / KGL_xxx)

**Run manually:**
```bash
python 03_data_integration.py
```

**Expected runtime:** 10-30 seconds

### Step 4: Analysis and Visualization

**Script:** `04_analysis_visualization.py`

**Input:**
- `data/integrated_data.csv`

**Outputs:**

**Tables** (JSON format in `results/tables/`):
- `descriptive_statistics.json` - Summary statistics by dataset
- `correlations.json` - Correlation coefficients
- `regression_results.json` - Regression models and coefficients
- `category_analysis.json` - ANOVA results by sleep category

**Figures** (PNG format in `results/figures/`):
- `01_sleep_distribution.png` - Histogram and category distribution
- `02_sleep_vs_performance.png` - Scatter plots and box plots
- `03_dataset_comparison.png` - CMU vs Kaggle comparison
- `04_productivity_mediation.png` - Mediation analysis visualizations

**Analyses performed:**
1. **Descriptive Statistics**
   - Mean, SD for sleep and academic performance
   - By dataset and overall

2. **Correlation Analysis**
   - Sleep ↔ Academic performance (overall, by dataset)
   - Sleep ↔ Productivity (Kaggle)
   - Productivity ↔ Academic (Kaggle)

3. **Regression Analysis**
   - Model 1: Academic ~ Sleep (all students)
   - Model 2: Academic ~ Sleep (CMU only)
   - Model 3: Academic ~ Sleep (Kaggle only)
   - Model 4: Mediation analysis (Kaggle only)

4. **Category Comparisons**
   - ANOVA across sleep categories
   - Post-hoc comparisons

**Run manually:**
```bash
python 04_analysis_visualization.py
```

**Expected runtime:** 1-2 minutes

---

## Automated Execution

### Option 1: Using Snakemake (Recommended)

Snakemake automatically manages dependencies and only re-runs steps when inputs change.

**Install Snakemake:**
```bash
pip install snakemake
```

**Run complete workflow:**
```bash
snakemake --cores 1
```

**Dry run (see what would execute):**
```bash
snakemake --cores 1 -n
```

**Force re-run everything:**
```bash
snakemake --cores 1 --forceall
```

**Clean outputs:**
```bash
snakemake clean
```

### Option 2: Using run_all.sh Script

A bash script that runs all steps sequentially.

**Make executable:**
```bash
chmod +x run_all.sh
```

**Run:**
```bash
./run_all.sh
```

**Clean and re-run:**
```bash
./run_all.sh --clean
```

**What it does:**
1. Checks prerequisites (Python, required files)
2. Creates output directories
3. Runs integration script
4. Runs analysis script
5. Verifies all outputs were created
6. Displays summary of results

---

## Manual Execution

If you prefer to run each step manually:

```bash
# Step 1: Integration
python 03_data_integration.py

# Step 2: Analysis
python 04_analysis_visualization.py

# Step 3: Verify outputs
ls data/integrated_data.csv
ls results/tables/
ls results/figures/
```

---

## Outputs

### Directory Structure

After running the complete workflow:

```
project-root/
├── data/
│   └── integrated_data.csv          # 1,547 students, 15 variables
├── results/
│   ├── tables/
│   │   ├── descriptive_statistics.json
│   │   ├── correlations.json
│   │   ├── regression_results.json
│   │   └── category_analysis.json
│   └── figures/
│       ├── 01_sleep_distribution.png
│       ├── 02_sleep_vs_performance.png
│       ├── 03_dataset_comparison.png
│       └── 04_productivity_mediation.png
└── logs/
    ├── integration.log
    └── analysis.log
```

### Output Descriptions

**integrated_data.csv:**
- 1,547 rows (students)
- 15 columns (variables)
- Combines CMU and Kaggle datasets
- Common variables: sleep_hours, academic_score, gender, sleep_category
- Dataset-specific variables preserved

**Analysis Tables:**
All in JSON format for easy parsing and reproducibility.

**Visualizations:**
All in 300 DPI PNG format, publication-quality.

---

## Reproducibility Checklist

To ensure someone else can reproduce your results:

- [ ] All scripts in repository (`03_data_integration.py`, `04_analysis_visualization.py`)
- [ ] Requirements.txt with package versions
- [ ] Snakefile for automated workflow
- [ ] run_all.sh for manual workflow
- [ ] This WORKFLOW.md documentation
- [ ] OpenRefine JSON recipe
- [ ] Cleaned input data (or instructions to obtain)
- [ ] Expected outputs documented
- [ ] Execution logs available

---

## Troubleshooting

### Common Issues

**1. "File not found" errors**

**Problem:** Script can't find input files  
**Solution:**
```bash
# Check you're in the right directory
pwd

# Check files exist
ls cleaned_cmu-sleep.csv
ls cleaned_student_habits.csv

# Check file paths in scripts match actual filenames
```

**2. "Module not found" errors**

**Problem:** Missing Python packages  
**Solution:**
```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn
# Or
pip install -r requirements.txt
```

**3. "Permission denied" for run_all.sh**

**Problem:** Script not executable  
**Solution:**
```bash
chmod +x run_all.sh
```

**4. Integration produces 0 rows**

**Problem:** Column names don't match expected  
**Solution:**
```bash
# Check column names in cleaned files
head -n 1 cleaned_cmu-sleep.csv
head -n 1 cleaned_student_habits.csv

# Compare with expected names in script
```

**5. Figures not generating**

**Problem:** Display backend issues (common on servers)  
**Solution:**
```python
# Add to top of script (before importing matplotlib.pyplot)
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
```

### Getting Help

1. **Check logs:**
   ```bash
   cat logs/integration.log
   cat logs/analysis.log
   ```

2. **Test scripts individually:**
   ```bash
   python 03_data_integration.py
   # If successful, then:
   python 04_analysis_visualization.py
   ```

3. **Verify Python environment:**
   ```bash
   python --version
   pip list | grep pandas
   pip list | grep numpy
   ```

---

## Expected Execution Times

On a typical laptop:

| Step | Time | Memory |
|------|------|--------|
| Integration | 10-30 sec | <500 MB |
| Analysis | 1-2 min | <1 GB |
| **Total** | **~2 min** | **<1 GB** |

---

## Validation

To verify your workflow ran correctly:

```bash
# Check file existence
test -f data/integrated_data.csv && echo "✓ Integration complete"
test -f results/tables/regression_results.json && echo "✓ Analysis complete"
test -f results/figures/01_sleep_distribution.png && echo "✓ Visualizations complete"

# Check file sizes (should not be empty)
ls -lh data/integrated_data.csv
ls -lh results/tables/*.json
ls -lh results/figures/*.png

# Preview results
head data/integrated_data.csv
cat results/tables/correlations.json | python -m json.tool
```

---

## Next Steps After Workflow Completion

1. **Review outputs** in `results/` directory
2. **Examine visualizations** for insights
3. **Read analysis logs** for detailed results
4. **Update README.md** with key findings
5. **Upload outputs to Box** for project submission
6. **Commit to Git** (excluding large data files)

---

## Contact

For questions about this workflow:
- **Authors:** Yamuna Nair and Monisha Mudunuri
- **Course:** IS 477 - Data Management
- **Date:** December 2025

---

**Last Updated:** December 2025  

