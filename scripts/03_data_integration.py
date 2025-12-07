"""
Data Integration Script for Sleep Patterns and Academic Performance Study
This script integrates the CMU Sleep dataset and Kaggle Student Habits dataset
to enable comprehensive analysis of sleep-performance relationships.

Author: [Your Name]
Date: December 2025
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime

# =====================================================
# STEP 1: LOAD CLEANED DATASETS
# =====================================================

print("=" * 70)
print("DATA INTEGRATION: Sleep Patterns & Academic Performance")
print("=" * 70)

# Load CMU cleaned data
try:
    cmu_df = pd.read_csv('data/processed/cleaned_cmu-sleep.csv')
    print(f"\n✓ CMU dataset loaded: {cmu_df.shape[0]} students, {cmu_df.shape[1]} variables")
except FileNotFoundError:
    print("\n✗ Error: CMU cleaned data not found at data/processed/cmu_clean.csv")
    print("  Please ensure cleaning step is completed first.")
    exit(1)

# Load Kaggle cleaned data
try:
    kaggle_df = pd.read_csv('data/processed/cleaned_student_habits.csv')
    print(f"✓ Kaggle dataset loaded: {kaggle_df.shape[0]} students, {kaggle_df.shape[1]} variables")
except FileNotFoundError:
    print("\n✗ Error: Kaggle cleaned data not found at data/processed/kaggle_clean.csv")
    print("  Please ensure cleaning step is completed first.")
    exit(1)

# =====================================================
# STEP 2: VARIABLE HARMONIZATION
# =====================================================

print("\n" + "=" * 70)
print("STEP 1: HARMONIZING VARIABLES")
print("=" * 70)

# --- CMU Dataset Transformations ---
print("\nCMU Dataset Transformations:")

# 2.1 Convert sleep time from minutes to hours
if 'TotalSleepTime' in cmu_df.columns:
    cmu_df['sleep_hours'] = cmu_df['TotalSleepTime'] / 60
    print(f"  ✓ Converted TotalSleepTime (minutes) → sleep_hours")
    print(f"    Range: {cmu_df['sleep_hours'].min():.2f}h to {cmu_df['sleep_hours'].max():.2f}h")
else:
    print("  ⚠ Warning: TotalSleepTime not found in CMU dataset")

# 2.2 Standardize GPA to 0-100 scale for comparison
if 'term_gpa' in cmu_df.columns:
    cmu_df['academic_score'] = (cmu_df['term_gpa'] / 4.0) * 100
    print(f"  ✓ Standardized term_gpa (0-4) → academic_score (0-100)")
else:
    print("  ⚠ Warning: term_gpa not found in CMU dataset")

# 2.3 Standardize gender coding (0/1 to Male/Female)
if 'demo_gender' in cmu_df.columns:
    cmu_df['gender'] = cmu_df['demo_gender'].map({0: 'Male', 1: 'Female'})
    print(f"  ✓ Standardized demo_gender (0/1) → gender (Male/Female)")

# 2.4 Create bedtime consistency variable
if 'bedtime_mssd' in cmu_df.columns:
    # Lower MSSD = more consistent bedtime
    # Log transform to reduce skew, then invert scale
    cmu_df['bedtime_consistency'] = -np.log1p(cmu_df['bedtime_mssd'])
    print(f"  ✓ Created bedtime_consistency from bedtime_mssd (higher = more consistent)")

# --- Kaggle Dataset Transformations ---
print("\nKaggle Dataset Transformations:")

# 2.5 Kaggle already has sleep_hours - verify it's clean
if 'sleep_hours' in kaggle_df.columns:
    print(f"  ✓ sleep_hours already present")
    print(f"    Range: {kaggle_df['sleep_hours'].min():.2f}h to {kaggle_df['sleep_hours'].max():.2f}h")

# 2.6 Kaggle has exam_score - already on 0-100 scale
if 'exam_score' in kaggle_df.columns:
    kaggle_df['academic_score'] = kaggle_df['exam_score']
    print(f"  ✓ Renamed exam_score → academic_score (0-100)")

# 2.7 Standardize gender (already Male/Female in Kaggle)
if 'gender' in kaggle_df.columns:
    print(f"  ✓ gender already standardized (Male/Female)")

# =====================================================
# STEP 3: CREATE DERIVED PRODUCTIVITY VARIABLES
# =====================================================

print("\n" + "=" * 70)
print("STEP 2: CREATING DERIVED VARIABLES")
print("=" * 70)

# For Kaggle dataset - create productivity metrics
print("\nKaggle Productivity Metrics:")

if all(col in kaggle_df.columns for col in ['social_media_hours', 'netflix_hours']):
    kaggle_df['distraction_hours'] = kaggle_df['social_media_hours'] + kaggle_df['netflix_hours']
    print(f"  ✓ Created distraction_hours (social_media + netflix)")
    print(f"    Mean: {kaggle_df['distraction_hours'].mean():.2f}h")

if all(col in kaggle_df.columns for col in ['study_hours_per_day', 'exam_score']):
    kaggle_df['study_efficiency'] = kaggle_df['exam_score'] / (kaggle_df['study_hours_per_day'] + 0.1)
    print(f"  ✓ Created study_efficiency (exam_score / study_hours)")
    print(f"    Mean: {kaggle_df['study_efficiency'].mean():.2f}")

if all(col in kaggle_df.columns for col in ['study_hours_per_day', 'attendance_percentage', 
                                              'distraction_hours', 'mental_health_rating']):
    # Composite productivity score (0-100 scale)
    kaggle_df['productivity_score'] = (
        (kaggle_df['study_hours_per_day'] / 12) * 25 +  # Study hours contribution
        (kaggle_df['attendance_percentage'] / 100) * 25 +  # Attendance contribution
        (1 - kaggle_df['distraction_hours'] / 24) * 25 +  # Distraction (inverted)
        (kaggle_df['mental_health_rating'] / 10) * 25    # Mental health contribution
    ) * 100
    print(f"  ✓ Created productivity_score (composite 0-100)")
    print(f"    Mean: {kaggle_df['productivity_score'].mean():.2f}")

# For CMU dataset - create sleep pattern categories
print("\nCMU Sleep Pattern Metrics:")

if 'sleep_hours' in cmu_df.columns:
    cmu_df['sleep_category'] = pd.cut(cmu_df['sleep_hours'],
                                      bins=[0, 6, 7, 8, 12],
                                      labels=['Poor', 'Insufficient', 'Adequate', 'Optimal'])
    print(f"  ✓ Created sleep_category (Poor/Insufficient/Adequate/Optimal)")
    print(f"    Distribution:\n{cmu_df['sleep_category'].value_counts()}")

# Create for Kaggle too
if 'sleep_hours' in kaggle_df.columns:
    kaggle_df['sleep_category'] = pd.cut(kaggle_df['sleep_hours'],
                                         bins=[0, 6, 7, 8, 12],
                                         labels=['Poor', 'Insufficient', 'Adequate', 'Optimal'])

# =====================================================
# STEP 4: SELECT COMMON VARIABLES FOR INTEGRATION
# =====================================================

print("\n" + "=" * 70)
print("STEP 3: SELECTING COMMON VARIABLES")
print("=" * 70)

# Define common variable schema
common_vars = {
    'student_id': 'str',      # Unique identifier
    'dataset_source': 'str',  # 'CMU' or 'Kaggle'
    'sleep_hours': 'float',   # Sleep duration in hours
    'academic_score': 'float', # Standardized academic performance (0-100)
    'gender': 'str',          # Male/Female
    'age': 'float'            # Age (if available)
}

print("\nCommon Integration Schema:")
for var, dtype in common_vars.items():
    print(f"  - {var}: {dtype}")

# Prepare CMU dataset for integration
cmu_integrated = pd.DataFrame()
cmu_integrated['student_id'] = 'CMU_' + cmu_df['subject_id'].astype(str)
cmu_integrated['dataset_source'] = 'CMU'
cmu_integrated['sleep_hours'] = cmu_df['sleep_hours'] if 'sleep_hours' in cmu_df.columns else np.nan
cmu_integrated['academic_score'] = cmu_df['academic_score'] if 'academic_score' in cmu_df.columns else np.nan
cmu_integrated['gender'] = cmu_df['gender'] if 'gender' in cmu_df.columns else np.nan
cmu_integrated['age'] = np.nan  # Not available in CMU dataset

# Add CMU-specific variables
if 'bedtime_consistency' in cmu_df.columns:
    cmu_integrated['bedtime_consistency'] = cmu_df['bedtime_consistency']
if 'daytime_sleep' in cmu_df.columns:
    cmu_integrated['daytime_sleep_minutes'] = cmu_df['daytime_sleep']
if 'cum_gpa' in cmu_df.columns:
    cmu_integrated['cumulative_gpa'] = cmu_df['cum_gpa']
if 'sleep_category' in cmu_df.columns:
    cmu_integrated['sleep_category'] = cmu_df['sleep_category']

# Prepare Kaggle dataset for integration
kaggle_integrated = pd.DataFrame()
kaggle_integrated['student_id'] = 'KGL_' + kaggle_df['student_id'].astype(str)
kaggle_integrated['dataset_source'] = 'Kaggle'
kaggle_integrated['sleep_hours'] = kaggle_df['sleep_hours'] if 'sleep_hours' in kaggle_df.columns else np.nan
kaggle_integrated['academic_score'] = kaggle_df['academic_score'] if 'academic_score' in kaggle_df.columns else np.nan
kaggle_integrated['gender'] = kaggle_df['gender'] if 'gender' in kaggle_df.columns else np.nan
kaggle_integrated['age'] = kaggle_df['age'] if 'age' in kaggle_df.columns else np.nan

# Add Kaggle-specific variables
if 'study_hours_per_day' in kaggle_df.columns:
    kaggle_integrated['study_hours_per_day'] = kaggle_df['study_hours_per_day']
if 'attendance_percentage' in kaggle_df.columns:
    kaggle_integrated['attendance_percentage'] = kaggle_df['attendance_percentage']
if 'productivity_score' in kaggle_df.columns:
    kaggle_integrated['productivity_score'] = kaggle_df['productivity_score']
if 'distraction_hours' in kaggle_df.columns:
    kaggle_integrated['distraction_hours'] = kaggle_df['distraction_hours']
if 'mental_health_rating' in kaggle_df.columns:
    kaggle_integrated['mental_health_rating'] = kaggle_df['mental_health_rating']
if 'sleep_category' in kaggle_df.columns:
    kaggle_integrated['sleep_category'] = kaggle_df['sleep_category']

print(f"\n✓ CMU data prepared: {cmu_integrated.shape}")
print(f"✓ Kaggle data prepared: {kaggle_integrated.shape}")

# =====================================================
# STEP 5: VERTICAL INTEGRATION (CONCATENATION)
# =====================================================

print("\n" + "=" * 70)
print("STEP 4: VERTICAL INTEGRATION (CONCATENATION)")
print("=" * 70)

# Concatenate datasets vertically
integrated_df = pd.concat([cmu_integrated, kaggle_integrated], 
                         axis=0, 
                         ignore_index=True,
                         sort=False)

print(f"\n✓ Datasets integrated successfully!")
print(f"  Total students: {len(integrated_df)}")
print(f"  CMU students: {(integrated_df['dataset_source'] == 'CMU').sum()}")
print(f"  Kaggle students: {(integrated_df['dataset_source'] == 'Kaggle').sum()}")
print(f"  Total variables: {integrated_df.shape[1]}")

# =====================================================
# STEP 6: DATA QUALITY CHECK ON INTEGRATED DATA
# =====================================================

print("\n" + "=" * 70)
print("STEP 5: POST-INTEGRATION QUALITY CHECK")
print("=" * 70)

print("\nMissing Values in Common Variables:")
common_cols = ['sleep_hours', 'academic_score', 'gender', 'age']
for col in common_cols:
    if col in integrated_df.columns:
        missing = integrated_df[col].isnull().sum()
        missing_pct = (missing / len(integrated_df)) * 100
        print(f"  {col}: {missing} ({missing_pct:.1f}%)")

print("\nSummary Statistics for Key Variables:")
if 'sleep_hours' in integrated_df.columns:
    print(f"\nSleep Hours:")
    print(f"  Overall: {integrated_df['sleep_hours'].mean():.2f}h ± {integrated_df['sleep_hours'].std():.2f}h")
    print(f"  CMU: {integrated_df[integrated_df['dataset_source']=='CMU']['sleep_hours'].mean():.2f}h")
    print(f"  Kaggle: {integrated_df[integrated_df['dataset_source']=='Kaggle']['sleep_hours'].mean():.2f}h")

if 'academic_score' in integrated_df.columns:
    print(f"\nAcademic Score (0-100):")
    print(f"  Overall: {integrated_df['academic_score'].mean():.2f} ± {integrated_df['academic_score'].std():.2f}")
    print(f"  CMU: {integrated_df[integrated_df['dataset_source']=='CMU']['academic_score'].mean():.2f}")
    print(f"  Kaggle: {integrated_df[integrated_df['dataset_source']=='Kaggle']['academic_score'].mean():.2f}")

# =====================================================
# STEP 7: SAVE INTEGRATED DATASET
# =====================================================

print("\n" + "=" * 70)
print("STEP 6: SAVING INTEGRATED DATASET")
print("=" * 70)

# Save integrated dataset
output_path = 'data/processed/integrated_data.csv'
integrated_df.to_csv(output_path, index=False)
print(f"\n✓ Integrated dataset saved to: {output_path}")

# Save separate dataset-specific files for targeted analyses
cmu_full_path = 'data/processed/cmu_enhanced.csv'
kaggle_full_path = 'data/processed/kaggle_enhanced.csv'

cmu_integrated.to_csv(cmu_full_path, index=False)
kaggle_integrated.to_csv(kaggle_full_path, index=False)

print(f"✓ CMU enhanced dataset saved to: {cmu_full_path}")
print(f"✓ Kaggle enhanced dataset saved to: {kaggle_full_path}")

# =====================================================
# STEP 8: CREATE INTEGRATION METADATA
# =====================================================

print("\n" + "=" * 70)
print("STEP 7: CREATING INTEGRATION METADATA")
print("=" * 70)

# Create metadata document
metadata = {
    "integration_date": datetime.now().isoformat(),
    "integration_method": "Vertical concatenation with source identifier",
    "source_datasets": {
        "CMU": {
            "n_students": int((integrated_df['dataset_source'] == 'CMU').sum()),
            "original_file": "data/processed/cmu_clean.csv",
            "unique_variables": ["bedtime_consistency", "daytime_sleep_minutes", "cumulative_gpa"]
        },
        "Kaggle": {
            "n_students": int((integrated_df['dataset_source'] == 'Kaggle').sum()),
            "original_file": "data/processed/kaggle_clean.csv",
            "unique_variables": ["study_hours_per_day", "attendance_percentage", 
                               "productivity_score", "distraction_hours", "mental_health_rating"]
        }
    },
    "common_variables": {
        "sleep_hours": "Sleep duration in hours (harmonized from CMU minutes and Kaggle hours)",
        "academic_score": "Academic performance on 0-100 scale (CMU GPA*25, Kaggle exam_score)",
        "gender": "Student gender (Male/Female)",
        "age": "Student age (available only in Kaggle)",
        "sleep_category": "Categorical sleep quality (Poor/Insufficient/Adequate/Optimal)"
    },
    "transformations_applied": [
        "CMU: TotalSleepTime (minutes) → sleep_hours (divided by 60)",
        "CMU: term_gpa (0-4) → academic_score (multiplied by 25)",
        "CMU: demo_gender (0/1) → gender (Male/Female)",
        "Kaggle: exam_score → academic_score (direct copy)",
        "Both: Created sleep_category from sleep_hours",
        "Kaggle: Created productivity_score composite metric",
        "CMU: Created bedtime_consistency from bedtime_mssd"
    ],
    "data_quality": {
        "total_students": int(len(integrated_df)),
        "missing_sleep_hours": int(integrated_df['sleep_hours'].isnull().sum()),
        "missing_academic_score": int(integrated_df['academic_score'].isnull().sum()),
        "missing_gender": int(integrated_df['gender'].isnull().sum())
    }
}

# Save metadata
metadata_path = 'data/metadata/integration_metadata.json'
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"\n✓ Integration metadata saved to: {metadata_path}")

# =====================================================
# STEP 9: CREATE INTEGRATION SCHEMA DIAGRAM
# =====================================================

print("\n" + "=" * 70)
print("STEP 8: INTEGRATION SCHEMA SUMMARY")
print("=" * 70)

print("""
INTEGRATION SCHEMA:

┌─────────────────────────────┐         ┌─────────────────────────────┐
│   CMU Sleep Dataset         │         │   Kaggle Habits Dataset     │
│  (634 students)             │         │  (1000 students)            │
├─────────────────────────────┤         ├─────────────────────────────┤
│ • TotalSleepTime (min)      │         │ • sleep_hours               │
│ • term_gpa (0-4)            │         │ • exam_score (0-100)        │
│ • demo_gender (0/1)         │         │ • gender (M/F)              │
│ • bedtime_mssd              │         │ • study_hours_per_day       │
│ • daytime_sleep             │         │ • attendance_percentage     │
│ • cum_gpa                   │         │ • mental_health_rating      │
└─────────────────────────────┘         └─────────────────────────────┘
              │                                     │
              │      HARMONIZATION &                │
              │      STANDARDIZATION                │
              ▼                                     ▼
        ┌──────────────────────────────────────────────┐
        │     INTEGRATED DATASET (1634 students)       │
        ├──────────────────────────────────────────────┤
        │  COMMON VARIABLES:                           │
        │  • student_id (with source prefix)           │
        │  • dataset_source (CMU/Kaggle)               │
        │  • sleep_hours (harmonized)                  │
        │  • academic_score (0-100 standardized)       │
        │  • gender (standardized)                     │
        │  • sleep_category (derived)                  │
        │                                              │
        │  DATASET-SPECIFIC VARIABLES:                 │
        │  • CMU: bedtime_consistency, cumulative_gpa  │
        │  • Kaggle: productivity_score, study_hours   │
        └──────────────────────────────────────────────┘
""")

print("\n" + "=" * 70)
print("✓ INTEGRATION COMPLETE!")
print("=" * 70)
print(f"\nOutputs generated:")
print(f"  1. {output_path} - Main integrated dataset")
print(f"  2. {cmu_full_path} - CMU enhanced dataset")
print(f"  3. {kaggle_full_path} - Kaggle enhanced dataset")
print(f"  4. {metadata_path} - Integration metadata")
print(f"\nReady for analysis!")
