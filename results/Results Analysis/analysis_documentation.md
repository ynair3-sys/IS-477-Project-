# Analysis Methods Documentation

**Project:** Sleep Patterns and Academic Performance Study  
**Script:** `04_analysis_visualization.py`  
**Date:** December 2025

---

## Overview

This document describes all statistical analyses and visualizations performed to answer our research question: **How do sleep patterns influence GPA and study productivity among college students?**

---

## Data Used

**Input:** `data/integrated_data.csv`
- **N = 1,547** students total
  - CMU subset: 547 students (objective Fitbit data)
  - Kaggle subset: 1,000 students (self-reported data)

**Key Variables:**
- `sleep_hours`: Sleep duration per night (continuous)
- `academic_score`: Academic performance, 0-100 scale (continuous)
- `sleep_category`: Sleep quality (categorical: Poor/Insufficient/Adequate/Optimal)
- `productivity_score`: Study productivity composite (continuous, Kaggle only)
- `dataset_source`: CMU or Kaggle (categorical)

---

## Statistical Analyses

### 1. Descriptive Statistics

**Purpose:** Characterize the sample and key variables

**Methods:**
```python
# Summary statistics
mean, std, min, max, median
# By dataset source (CMU vs Kaggle)
# By sleep category
```

**Output:** `results/tables/descriptive_statistics.json`

**Key Metrics:**
- Sleep duration: Overall, by dataset
- Academic performance: Overall, by dataset
- Distribution of sleep categories
- Sample sizes for each group

### 2. Correlation Analysis

**Purpose:** Examine bivariate relationships between variables

**Methods:**
- Pearson correlation coefficient (r)
- Computed for all students and by dataset

**Relationships examined:**
1. Sleep hours ↔ Academic score
   - Overall (N=1,547)
   - CMU only (N=547)
   - Kaggle only (N=1,000)

2. Additional (Kaggle only, N=1,000):
   - Sleep hours ↔ Productivity score
   - Productivity score ↔ Academic score

**Output:** `results/tables/correlations.json`

**Interpretation:**
- r > 0.3: Moderate positive correlation
- r > 0.5: Strong positive correlation
- p < 0.05: Statistically significant

### 3. Regression Analysis

**Purpose:** Quantify the effect of sleep on academic performance

#### Model 1: Simple Linear Regression (All Students)

```
Academic Score = β₀ + β₁(Sleep Hours) + ε
```

**Sample:** N = 1,547 (all students)

**Interpretation:**
- **β₁ coefficient**: Change in academic score per 1-hour increase in sleep
- **R²**: Proportion of variance in academic score explained by sleep
- **RMSE**: Average prediction error

#### Model 2: CMU Subset

```
Academic Score = β₀ + β₁(Sleep Hours) + ε
```

**Sample:** N = 547 (CMU students with objective Fitbit data)

**Purpose:** Test relationship using objective sleep measurement

#### Model 3: Kaggle Subset

```
Academic Score = β₀ + β₁(Sleep Hours) + ε
```

**Sample:** N = 1,000 (Kaggle students with self-reported data)

**Purpose:** Test relationship using self-reported measures

#### Model 4: Mediation Analysis (Kaggle Only)

**Purpose:** Test if productivity mediates sleep → academic performance relationship

**Framework:**
```
Path A: Sleep Hours → Productivity Score
Path B: Productivity Score → Academic Score (controlling for sleep)
Path C: Sleep Hours → Academic Score (total effect)
Path C': Sleep Hours → Academic Score (controlling for productivity)
```

**Mediation test:**
- Indirect effect = Path A × Path B
- Proportion mediated = (Indirect effect) / (Total effect)

**Sample:** N = 1,000 (Kaggle only - has productivity measures)

**Interpretation:**
- If proportion mediated > 0.3: Strong mediation
- Indicates sleep works through improved productivity

**Output:** `results/tables/regression_results.json`

### 4. Group Comparisons (ANOVA)

**Purpose:** Compare academic performance across sleep categories

**Method:** One-way ANOVA

```
H₀: μ_poor = μ_insufficient = μ_adequate = μ_optimal
H₁: At least one mean differs
```

**Groups:**
- Poor sleep (<6 hours)
- Insufficient sleep (6-7 hours)
- Adequate sleep (7-8 hours)
- Optimal sleep (>8 hours)

**Follow-up:** If significant (p < 0.05), compute means by category

**Output:** `results/tables/category_analysis.json`

---

## Visualizations

All figures saved to `results/figures/` in 300 DPI PNG format.

### Figure 1: Sleep Distribution

**File:** `01_sleep_distribution.png`

**Components:**
- **Left panel:** Histogram of sleep hours
  - Shows distribution shape (normal, skewed?)
  - Mean line (red dashed)
  - Recommended 7h line (green dotted)
  
- **Right panel:** Bar chart of sleep categories
  - Count and percentage for each category
  - Color-coded by severity (red=Poor, blue=Optimal)

**Purpose:** Describe overall sleep patterns in sample

### Figure 2: Sleep vs Performance

**File:** `02_sleep_vs_performance.png`

**Components:**
- **Left panel:** Scatter plot with regression line
  - X-axis: Sleep hours
  - Y-axis: Academic score
  - Regression line with equation and R²
  
- **Right panel:** Box plots by sleep category
  - Shows distribution and outliers
  - Enables visual comparison across categories

**Purpose:** Visualize primary research question

### Figure 3: Dataset Comparison

**File:** `03_dataset_comparison.png`

**Components:**
- **Left panel:** Sleep hours by dataset
  - CMU (Fitbit) vs Kaggle (self-report)
  - Box plots with means
  
- **Right panel:** Academic scores by dataset
  - Shows any systematic differences
  - Important for interpretation

**Purpose:** Assess dataset differences for comparative analysis

### Figure 4: Productivity Mediation

**File:** `04_productivity_mediation.png`

**Components (2×2 grid):**
- **Top-left:** Sleep → Productivity scatter
- **Top-right:** Productivity → Academic scatter
- **Bottom-left:** Study hours by sleep category
- **Bottom-right:** Attendance by sleep category

**Purpose:** Visualize mediation pathway and mechanisms

---

## Interpretation Guidelines

### Statistical Significance

- **p < 0.05**: Statistically significant (reject null hypothesis)
- **p < 0.01**: Highly significant
- **p < 0.001**: Very highly significant

### Effect Sizes

**For correlations:**
- |r| < 0.3: Weak
- 0.3 ≤ |r| < 0.5: Moderate
- |r| ≥ 0.5: Strong

**For regression:**
- R² < 0.10: Small amount of variance explained
- 0.10 ≤ R² < 0.30: Moderate
- R² ≥ 0.30: Substantial

**For means:**
- Cohen's d < 0.5: Small difference
- 0.5 ≤ d < 0.8: Medium
- d ≥ 0.8: Large

### Practical Significance

Beyond statistical significance, consider:
- **Magnitude:** Is the effect size meaningful?
- **Context:** Does it matter in real-world terms?
- **Example:** A 2-point increase in academic score per hour of sleep may be statistically significant but relatively small in magnitude

---

## Limitations

### Statistical Limitations

1. **Observational data:** Cannot infer causation
   - Sleep might affect GPA, OR
   - GPA might affect sleep, OR
   - A third variable might cause both

2. **Cross-sectional:** Single time point
   - Cannot assess temporal dynamics
   - Cannot rule out reverse causality

3. **Selection bias:** 
   - CMU students may differ systematically from Kaggle
   - Both samples may not represent all college students

4. **Measurement error:**
   - Self-report bias in Kaggle data
   - Fitbit accuracy limitations in CMU data

### Analytical Limitations

1. **Missing data:**
   - Productivity variables only in Kaggle (N=1,000)
   - Detailed sleep patterns only in CMU (N=547)
   - Full mediation analysis limited to Kaggle subset

2. **Confounding:**
   - Cannot control for all potential confounders
   - e.g., motivation, stress, course difficulty

3. **Scale differences:**
   - CMU: GPA scaled to 0-100
   - Kaggle: Exam scores 0-100
   - May not be directly comparable

---

## Quality Checks

### Data Validation

Before analysis, script validates:
- [ ] File exists and loads successfully
- [ ] Required variables present
- [ ] No completely missing variables
- [ ] Sample sizes match expected

### Analysis Validation

Script includes checks for:
- [ ] No NaN values in key calculations
- [ ] Sample sizes reported for each analysis
- [ ] Regression models converge successfully
- [ ] All output files created

### Output Validation

After running, verify:
- [ ] 4 JSON files in results/tables/
- [ ] 4 PNG files in results/figures/
- [ ] Log file shows no errors
- [ ] Results make sense (e.g., correlations between -1 and 1)

---

## Reproducibility

### Random Seeds

No random processes used - all analyses are deterministic.

### Software Versions

Record package versions for reproducibility:
```bash
pip freeze > requirements_freeze.txt
```

### Execution Environment

Document:
- Python version: `python --version`
- Operating system: `uname -a` (Unix) or `systeminfo` (Windows)
- Date executed: Logged in output files

---

## Expected Results

### Hypothesized Relationships

Based on literature, we expect:

1. **Positive correlation** between sleep and academic performance
   - r ≈ 0.2 to 0.4 (moderate)

2. **Dose-response relationship** across sleep categories
   - Poor < Insufficient < Adequate < Optimal

3. **Mediation through productivity**
   - Sleep → Better study habits → Higher grades
   - Partial mediation (not complete)

4. **Objective vs self-report**
   - CMU effects may be stronger (less measurement error)
   - Kaggle may show social desirability bias

### Interpreting Unexpected Results

If results differ from expectations:
- Check for errors in code/data
- Consider alternative explanations
- Discuss in limitations section
- Suggest future research directions

---

## Usage

### Running the Analysis

```bash
python 04_analysis_visualization.py
```

### Reading the Outputs

**JSON files:**
```python
import json

# Load results
with open('results/tables/regression_results.json') as f:
    results = json.load(f)

# Access specific model
model1 = results['model_1_simple']
print(f"Sleep coefficient: {model1['coefficient']:.2f}")
```

**Figures:**
Open PNG files in any image viewer or include in reports.


