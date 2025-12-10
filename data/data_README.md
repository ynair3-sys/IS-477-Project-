# Data

This folder contains all data files organized by processing stage and also includes all OpenRefine recipes in json format. 

## Subfolders

### raw/
- **Purpose:** Original, unmodified datasets as downloaded
- **Files:**
  - `cmu-sleep.csv` - CMU Sleep and GPA dataset (634 students)
  - `student_habits_performance.csv` - Kaggle Student Habits dataset (1,000 students)
- **Workflow Step:** Data acquisition
- **Note:** Raw data preserved for reproducibility

### processed/
- **Purpose:** Cleaned datasets after OpenRefine processing
- **Files:**
  - `cleaned_cmu-sleep.csv` - Cleaned CMU dataset
  - `cleaned_student_habits.csv` - Cleaned Kaggle dataset
- **Workflow Step:** Data cleaning
- **Cleaning:** Missing values handled, duplicates removed, standardized formats

### integrated/
- **Purpose:** Merged dataset combining both sources
- **Files:**
  - `integrated_data.csv` - Complete integrated dataset (1,547 students, 15 variables)
- **Workflow Step:** Data integration
- **Content:**
  - Common variables: sleep_hours, academic_score, gender, sleep_category
  - Dataset-specific variables preserved
  - Source identifier: dataset_source (CMU/Kaggle)

---

## Data Flow

```
raw/ → processed/ → integrated/ → (used by analysis scripts)
  ↓        ↓            ↓
634 +   1,000 →     1,547 students
CMU    Kaggle      Combined
```

---

## What These Files Support

**Transparency:**
- Raw data preserved (shows original state)
- Processed data documented (shows cleaning)
- Integrated data available (shows merging)
- Complete data pipeline visible

**Reproducibility :**
- All data stages available for verification
- Cleaning steps can be validated
- Integration process can be reproduced

---

**Data Sources:**
- **CMU:** https://cmustatistics.github.io/data-repository/data/cmu-sleep.csv
- **Kaggle:** https://www.kaggle.com/datasets/jayaantanaath/student-habits-vs-academic-performance

**Data Documentation:** See `../Documentation Files/Data Dictionary.pdf`

---

**Navigation:**
- Project root: `../`
- Scripts: `../scripts/`
- Results: `../results/`
