# Reproducibility Documentation

This document provides comprehensive information to allow independent reproduction of our sleep and academic performance analysis workflow.

---

## Project Overview

**Title**: Sleep Patterns and Academic Performance Among College Students

**Authors**: Yamuna Nair and Monisha Mudunuri

**Course**: IS 477 - Data Management & Curation

**Date**: December 2025

**Research Question**: How do sleep patterns influence GPA and study productivity among college students?

---

## Complete Workflow Documentation

### 1. Data Acquisition

#### Dataset 1: CMU Sleep and GPA Dataset

**Source**: Carnegie Mellon University Sleep Study  
**Original URL**: [Provide actual URL or repository location]  
**Access Date**: 9/24/25 
**Format**: CSV  
**License**: Open academic research license (Creative Commons Attribution 4.0)

**Original Variables**:
- `TotalSleepTime` - Total sleep duration in minutes
- `GPA` - Semester GPA on 0.0-4.0 scale
- Student demographics (anonymized)

**Download Method**: Direct download from public repository with SHA-256 checksum verification

#### Dataset 2: Kaggle Student Habits Dataset

**Source**: Kaggle community dataset by Jayanta Nath  
**URL**: https://www.kaggle.com/datasets/jayaantanaath/student-habits-vs-academic-performance  
**Access Date**: 9/24/25
**Format**: CSV  
**License**: Kaggle Community License, Apache 2.0

**Original Variables**:
- `sleep_hours` - Self-reported average sleep per night
- `exam_score` - Final exam score (0-100)
- `study_hours_per_day` - Daily study time
- `attendance_percentage` - Class attendance rate
- `social_media_hours` - Daily social media usage
- `netflix_hours` - Daily streaming time
- `mental_health_rating` - Self-reported mental health (1-10)

**Download Method**: Manual download from Kaggle platform (requires free account)

---

### 2. Data Cleaning and Preprocessing

**Tool Used**: OpenRefine 3.7.6

**Cleaning Operations Applied**:

**For CMU Dataset**:
1. Removed duplicate rows (if any)
2. Converted `TotalSleepTime` from minutes to hours: `sleep_hours = TotalSleepTime / 60`
3. Scaled GPA to 0-100 scale: `academic_score = GPA * 25`
4. Removed rows with missing sleep or GPA values
5. Standardized column names to lowercase with underscores
6. Trimmed whitespace from all text fields
7. Added `dataset_source = "CMU"` column

**For Kaggle Dataset**:
1. Removed duplicate rows based on student_id
2. Renamed `exam_score` to `academic_score` for consistency
3. Calculated derived variable: `distraction_hours = social_media_hours + netflix_hours`
4. Created productivity score: 
   ```
   productivity_score = (study_hours_per_day * 0.3 + 
                         attendance_percentage * 0.3 + 
                         (10 - distraction_hours) * 0.2 + 
                         mental_health_rating * 0.2)
   ```
5. Removed rows with missing values in key variables
6. Validated numeric ranges (sleep_hours: 3-10, exam_score: 0-100)
7. Trimmed whitespace from all text fields
8. Added `dataset_source = "Kaggle"` column

**Output Files**:
- `data/processed/cleaned_cmu_sleep.csv` (547 rows × 3 columns)
- `data/processed/cleaned_kaggle_habits.csv` (1000 rows × 4 columns)

**Data Validation**:
- Checked for outliers using IQR method
- Verified no duplicate student records
- Confirmed all numeric values within expected ranges
- Ensured no missing values in critical columns

---

### 3. Data Integration

**Script**: `scripts/01_integrate_data.py`

**Integration Method**: Vertical concatenation (stacking datasets)

**Steps**:
1. Load both cleaned datasets
2. Add `productivity_score` column to CMU data (set to NaN - not available)
3. Concatenate datasets using `pd.concat()` with `ignore_index=True`
4. Create sleep categories using `pd.cut()`:
   - **Poor**: < 6 hours
   - **Insufficient**: 6-7 hours
   - **Adequate**: 7-8 hours
   - **Optimal**: > 8 hours
5. Save integrated dataset

**Output**: `data/processed/integrated_data.csv` (1547 rows × 5 columns)

**Schema of Integrated Dataset**:
```
Column Name          Data Type    Description
-----------------    ---------    ----------------------------------
sleep_hours          float64      Sleep duration per night (hours)
academic_score       float64      Academic performance (0-100 scale)
dataset_source       object       "CMU" or "Kaggle"
productivity_score   float64      Composite productivity metric (Kaggle only)
sleep_category       category     Poor/Insufficient/Adequate/Optimal
```

---

### 4. Statistical Analysis

**Script**: `scripts/02_analysis.py`

**Software Environment**:
- Python 3.8+
- pandas 2.0.3
- numpy 1.24.3
- scipy 1.11.1
- scikit-learn 1.3.0

**Analyses Performed**:

#### 4.1 Descriptive Statistics

**Method**: Calculated mean, standard deviation, and sample size for:
- Sleep hours (overall, by dataset)
- Academic scores (overall, by dataset)
- Sleep category distribution

**Output**: `results/tables/descriptive_statistics.json`

**Key Results**:
- Overall: N=1547, Mean sleep=6.52h (SD=1.11), Mean academic=75.55 (SD=17.36)
- CMU: N=547, Mean sleep=6.61h (SD=0.85), Mean academic=86.41 (SD=12.17)
- Kaggle: N=1000, Mean sleep=6.47h (SD=1.23), Mean academic=69.60 (SD=16.89)

#### 4.2 Correlation Analysis

**Method**: Pearson correlation coefficient using `pandas.DataFrame.corr()`

**Variables Analyzed**:
1. Sleep hours ↔ Academic score (overall, by dataset)
2. Sleep hours ↔ Productivity score (Kaggle only)
3. Productivity score ↔ Academic score (Kaggle only)

**Output**: `results/tables/correlations.json`

**Key Results**:
- Overall sleep-academic correlation: r = 0.144
- CMU sleep-academic correlation: r = 0.161
- Kaggle sleep-academic correlation: r = 0.122
- Sleep-productivity correlation: r = -0.015
- Productivity-academic correlation: r = 0.659

**Statistical Significance**: All correlations tested at α = 0.05 level

#### 4.3 Regression Analysis

**Method**: Ordinary Least Squares (OLS) linear regression using `sklearn.linear_model.LinearRegression`

**Models Fitted**:

**Model 1: Overall Effect (N=1547)**
```
academic_score = β₀ + β₁(sleep_hours) + ε

Results:
- Coefficient (β₁): 2.25 points per hour
- Intercept (β₀): 60.87
- R²: 0.021
- RMSE: 17.17
```

**Model 2: CMU Subset (N=547)**
```
academic_score = β₀ + β₁(sleep_hours) + ε

Results:
- Coefficient (β₁): 2.30 points per hour
- Intercept (β₀): 71.21
- R²: 0.026
- RMSE: 12.00
```

**Model 3: Kaggle Subset (N=1000)**
```
academic_score = β₀ + β₁(sleep_hours) + ε

Results:
- Coefficient (β₁): 1.68 points per hour
- Intercept (β₀): 58.76
- R²: 0.015
- RMSE: 16.75
```

**Model 4: Mediation Analysis (N=1000, Kaggle only)**

Testing whether productivity mediates the sleep → academic performance relationship

**Paths Tested**:
- Path A: Sleep → Productivity (β = -9.80)
- Path B: Productivity → Academic (controlling for sleep) (β = 0.014)
- Path C: Sleep → Academic (total effect) (β = 1.68)
- Path C': Sleep → Academic (direct effect) (β = 1.81)

**Mediation Results**:
- Indirect effect: -0.133
- Proportion mediated: -0.079 (negative indicates no mediation)

**Interpretation**: Productivity does not mediate the sleep-performance relationship in our sample.

**Output**: `results/tables/regression_results.json`

#### 4.4 Group Comparisons (ANOVA)

**Method**: 

**Null Hypothesis**: Mean academic scores are equal across all sleep categories

**Groups**:
1. Poor (<6h): N=489, Mean=71.31 (SD=17.25)
2. Insufficient (6-7h): N=567, Mean=77.33 (SD=17.18)
3. Adequate (7-8h): N=363, Mean=78.77 (SD=16.47)
4. Optimal (>8h): N=128, Mean=74.65 (SD=17.94)

**Results**:
- F-statistic: 16.49
- p-value: 1.50 × 10⁻¹⁰
- Conclusion: Reject null hypothesis (p < 0.001)

**Output**: `results/tables/category_analysis.json`

---

### 5. Visualizations

**Script**: `scripts/03_analysis_visualizations.py`

**Software Environment**:
- matplotlib 3.7.2
- seaborn 0.12.2

**Figures Generated**:

#### Figure 1: Sleep Distribution (`01_sleep_distribution.png`)

**Type**: Histogram + Bar chart  
**Purpose**: Describe overall sleep patterns in sample  
**Components**:
- Left panel: Histogram of sleep hours (20 bins)
  - Red dashed line: Mean sleep (6.52h)
  - Green dotted line: Recommended sleep (7h)
- Right panel: Bar chart of sleep categories
  - Counts and percentages for each category
  - Color-coded by severity

**Parameters**:
- Figure size: 14×5 inches
- DPI: 300
- Style: whitegrid

#### Figure 2: Sleep vs Performance (`02_sleep_vs_performance.png`)

**Type**: Scatter plot + Box plots  
**Purpose**: Visualize primary research question  
**Components**:
- Left panel: Scatter plot with OLS regression line
  - Each dot = one student (N=1547)
  - Red line: Best-fit linear regression
  - Equation and R² displayed
- Right panel: Box plots by sleep category
  - Shows median, quartiles, and outliers
  - Color-coded by category

**Parameters**:
- Alpha transparency: 0.3 for scatter points
- Regression line width: 2
- Figure size: 14×5 inches
- DPI: 300

#### Figure 3: Dataset Comparison (`03_dataset_comparison.png`)

**Type**: Side-by-side box plots  
**Purpose**: Compare CMU (objective) vs Kaggle (self-report) measurements  
**Components**:
- Left panel: Sleep hours by dataset
  - CMU (blue box): Fitbit data
  - Kaggle (coral box): Self-report data
  - Green triangles: Mean values
- Right panel: Academic scores by dataset
  - CMU: GPA scaled to 0-100
  - Kaggle: Exam scores

**Parameters**:
- Box width: 0.6
- Mean marker: Green triangle
- Figure size: 14×5 inches
- DPI: 300

#### Figure 4: Productivity Mediation (`04_productivity_mediation.png`)

**Type**: 2×2 grid of scatter plots and bar charts  
**Purpose**: Visualize mediation analysis pathways  
**Components**:
- Top-left: Sleep → Productivity (r = -0.015)
- Top-right: Productivity → Academic (r = 0.659)
- Bottom-left: Study hours by sleep category (bar chart)
- Bottom-right: Attendance by sleep category (bar chart)

**Parameters**:
- Figure size: 14×10 inches
- Scatter alpha: 0.4
- DPI: 300

**All Figures Specifications**:
- File format: PNG
- Resolution: 300 DPI (publication quality)
- Color palette: Consistent across all figures
- Font sizes: Title=16pt, Labels=12pt, Ticks=10pt

---

### 6. Computational Environment

**Operating System**: [Your OS, e.g., macOS 13.5, Ubuntu 22.04, Windows 11]

**Python Version**: 3.8.10 (or higher)

**Required Packages** (exact versions):
```
pandas==2.0.3
numpy==1.24.3
matplotlib==3.7.2
seaborn==0.12.2
scipy==1.11.1
scikit-learn==1.3.0
```

**Installation Instructions**:
```bash
pip install -r requirements.txt
```

**Hardware Requirements**:
- Minimum: 4GB RAM, 2GB disk space


---

### 7. Execution Instructions

**Step-by-step reproduction**:

```bash
# 1. Clone or download project
git clone [repository_url]
cd sleep-gpa-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify data files exist
ls data/processed/

# Expected files:
# - cleaned_cmu_sleep.csv
# - cleaned_kaggle_habits.csv

# 4. Run integration
python scripts/01_integrate_data.py

# Expected output: data/processed/integrated_data.csv

# 5. Run analysis
python scripts/02_analysis.py

# Expected outputs in results/tables/:
# - descriptive_statistics.json
# - correlations.json
# - regression_results.json
# - category_analysis.json

# 6. Generate visualizations
python scripts/03_visualizations.py

# Expected outputs in results/figures/:
# - 01_sleep_distribution.png
# - 02_sleep_vs_performance.png
# - 03_dataset_comparison.png
# - 04_productivity_mediation.png

# 7. Verify outputs
ls results/tables/
ls results/figures/
```

**Expected execution time**: 30-40 seconds total

---

**Data License**: 
- CMU dataset: CC-BY-4.0
- Kaggle dataset: Kaggle Community License
- Our cleaned/processed data: CC-BY-4.0

---

### 10. Validation Checksums

**File Integrity Verification**:

Use SHA-256 checksums to verify data integrity:

```bash
# Generate checksums
sha256sum data/processed/cleaned_cmu_sleep.csv
sha256sum data/processed/cleaned_kaggle_habits.csv
sha256sum data/processed/integrated_data.csv
```

**Expected checksums** (store these after initial run):
```
[Your SHA-256 hash]  cleaned_cmu_sleep.csv
[Your SHA-256 hash]  cleaned_kaggle_habits.csv
[Your SHA-256 hash]  integrated_data.csv
```

---

### 11. Expected Results

**Key numerical results to verify reproduction**:

| Metric | Expected Value | Tolerance |
|--------|---------------|-----------|
| Total sample size | 1547 | Exact |
| Mean sleep hours | 6.52 | ±0.01 |
| Mean academic score | 75.55 | ±0.01 |
| Overall correlation (r) | 0.144 | ±0.001 |
| Regression coefficient | 2.25 | ±0.01 |
| R² | 0.021 | ±0.001 |
| ANOVA F-statistic | 16.49 | ±0.01 |
| ANOVA p-value | < 0.001 | N/A |
| Poor sleep count | 489 | Exact |
| Insufficient sleep count | 567 | Exact |

**If your results differ**: Check that you're using the exact cleaned datasets from Box and the specified package versions.

---

### 12. Known Limitations and Assumptions

**Data Limitations**:
1. **Different measurement scales**: CMU uses GPA, Kaggle uses exam scores
2. **Different populations**: CMU is three specific universities, Kaggle source is unclear
3. **Self-report bias**: Kaggle data relies on self-reported sleep
4. **Cross-sectional design**: Cannot infer causation
5. **Missing productivity data**: Only available for Kaggle subset

**Analysis Assumptions**:
1. Linear relationship between sleep and academic performance
2. Independence of observations (each student counted once)
3. Missing data is missing at random
4. GPA-to-100 scale conversion is appropriate (GPA × 25)
5. Sleep categories reflect meaningful psychological differences

**Reproducibility Notes**:
1. OpenRefine cleaning cannot be fully scripted - we provide cleaned data
2. Minor visualization differences may occur with different matplotlib versions
3. Random seed not applicable (no stochastic processes)
4. Floating-point arithmetic may cause tiny differences across platforms

---

### 13. Troubleshooting

**Common Issues**:

| Issue | Cause | Solution |
|-------|-------|----------|
| Module not found | Missing dependencies | Run `pip install -r requirements.txt` |
| File not found | Wrong directory | Verify you're in project root |
| Different results | Wrong data version | Download cleaned data from Box |
| Encoding errors | Wrong file encoding | Specify `encoding='utf-8'` in read_csv |
| Memory error | Insufficient RAM | Close other applications |

**Getting Help**:
1. Check error message carefully
2. Verify all file paths are correct
3. Confirm package versions match exactly

---

## 14. Reproducibility Checklist

Use this checklist to verify complete reproducibility:

- [ ] All raw data sources documented with URLs and access dates
- [ ] Data cleaning steps fully documented (OpenRefine log provided)
- [ ] Cleaned datasets available via Box with stable link
- [ ] All analysis scripts provided with inline comments
- [ ] Python environment fully specified (requirements.txt)
- [ ] Directory structure clearly documented
- [ ] Execution instructions tested by independent user
- [ ] Expected results provided with tolerance ranges
- [ ] SHA-256 checksums provided for data files
- [ ] All figures reproducible at 300 DPI
- [ ] Statistical methods clearly described
- [ ] Limitations and assumptions documented
- [ ] Troubleshooting guide provided
- [ ] Contact information for authors provided
- [ ] License information included

---

**This document provides all information necessary for independent reproduction of our analysis from data acquisition through final results.**
