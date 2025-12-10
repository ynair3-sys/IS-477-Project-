"""
Data Integration Script - Sleep Patterns and Academic Performance
Integrates CMU Sleep dataset with Kaggle Student Habits dataset

Author: [Your Name]
Date: December 2025
"""

import pandas as pd
import numpy as np
import os

# File paths
CMU_PATH = "cleaned_cmu-sleep.csv"
KAGGLE_PATH = "cleaned_student_habits.csv"

def load_cmu(csv_file):
    """Load and standardize CMU Sleep dataset"""
    df = pd.read_csv(csv_file)
    
    # Convert sleep from minutes to hours
    df['sleep_hours'] = df['TotalSleepTime'] / 60
    
    # Convert GPA (0-4 scale) to 0-100 scale
    df['academic_score'] = (df['term_gpa'] / 4.0) * 100
    
    # Convert gender from 0/1 to Male/Female
    df['gender'] = df['demo_gender'].map({0: 'Male', 1: 'Female'})
    
    # Create sleep quality categories
    df['sleep_category'] = pd.cut(
        df['sleep_hours'],
        bins=[0, 6, 7, 8, 12],
        labels=['Poor', 'Insufficient', 'Adequate', 'Optimal']
    )
    
    # Select and rename columns for integration
    df = df.rename(columns={
        'subject_id': 'student_id',
        'bedtime_mssd': 'bedtime_variability',
        'cum_gpa': 'cumulative_gpa'
    })
    
    return df

def load_kaggle(csv_file):
    """Load and standardize Kaggle Student Habits dataset"""
    df = pd.read_csv(csv_file)
    
    # Rename for consistency
    df['academic_score'] = df['exam_score']
    
    # Create sleep quality categories
    df['sleep_category'] = pd.cut(
        df['sleep_hours'],
        bins=[0, 6, 7, 8, 12],
        labels=['Poor', 'Insufficient', 'Adequate', 'Optimal']
    )
    
    # Create derived productivity variables
    df['distraction_hours'] = df['social_media_hours'] + df['netflix_hours']
    
    df['productivity_score'] = (
        (df['study_hours_per_day'] / 12) * 25 +
        (df['attendance_percentage'] / 100) * 25 +
        (1 - df['distraction_hours'] / 24) * 25 +
        (df['mental_health_rating'] / 10) * 25
    ) * 100
    
    return df

def integrate_datasets(cmu_df, kaggle_df):
    """Integrate CMU and Kaggle datasets using append method"""
    
    # Prepare CMU data for integration
    cmu_integrated = pd.DataFrame()
    cmu_integrated['student_id'] = 'CMU_' + cmu_df['student_id'].astype(str)
    cmu_integrated['dataset_source'] = 'CMU'
    cmu_integrated['sleep_hours'] = cmu_df['sleep_hours']
    cmu_integrated['academic_score'] = cmu_df['academic_score']
    cmu_integrated['gender'] = cmu_df['gender']
    cmu_integrated['sleep_category'] = cmu_df['sleep_category']
    cmu_integrated['integration_method'] = 'append'
    
    # CMU-specific variables
    cmu_integrated['bedtime_variability'] = cmu_df['bedtime_variability']
    cmu_integrated['cumulative_gpa'] = cmu_df['cumulative_gpa']
    cmu_integrated['age'] = pd.NA
    cmu_integrated['study_hours_per_day'] = pd.NA
    cmu_integrated['attendance_percentage'] = pd.NA
    cmu_integrated['productivity_score'] = pd.NA
    cmu_integrated['distraction_hours'] = pd.NA
    
    # Prepare Kaggle data for integration
    kaggle_integrated = pd.DataFrame()
    kaggle_integrated['student_id'] = 'KGL_' + kaggle_df['student_id'].astype(str)
    kaggle_integrated['dataset_source'] = 'Kaggle'
    kaggle_integrated['sleep_hours'] = kaggle_df['sleep_hours']
    kaggle_integrated['academic_score'] = kaggle_df['academic_score']
    kaggle_integrated['gender'] = kaggle_df['gender']
    kaggle_integrated['sleep_category'] = kaggle_df['sleep_category']
    kaggle_integrated['integration_method'] = 'append'
    
    # Kaggle-specific variables
    kaggle_integrated['age'] = kaggle_df['age']
    kaggle_integrated['study_hours_per_day'] = kaggle_df['study_hours_per_day']
    kaggle_integrated['attendance_percentage'] = kaggle_df['attendance_percentage']
    kaggle_integrated['productivity_score'] = kaggle_df['productivity_score']
    kaggle_integrated['distraction_hours'] = kaggle_df['distraction_hours']
    kaggle_integrated['bedtime_variability'] = pd.NA
    kaggle_integrated['cumulative_gpa'] = pd.NA
    
    # Combine datasets vertically (append)
    final = pd.concat([cmu_integrated, kaggle_integrated], ignore_index=True)
    
    # Add record ID and sort
    final.insert(0, 'record_id', range(1, len(final) + 1))
    final = final.sort_values('sleep_hours', na_position='last')
    
    return final

def main():
    print("=" * 70)
    print("DATA INTEGRATION: Sleep Patterns & Academic Performance")
    print("=" * 70)
    
    # Load datasets
    print("\n[1/3] Loading datasets...")
    cmu = load_cmu(CMU_PATH)
    print(f"  ✓ CMU: {len(cmu)} students loaded and standardized")
    
    kaggle = load_kaggle(KAGGLE_PATH)
    print(f"  ✓ Kaggle: {len(kaggle)} students loaded and standardized")
    
    # Integrate datasets
    print("\n[2/3] Integrating datasets...")
    integrated = integrate_datasets(cmu, kaggle)
    print(f"  ✓ Integration complete: {len(integrated)} total students")
    print(f"    - CMU: {(integrated['dataset_source'] == 'CMU').sum()}")
    print(f"    - Kaggle: {(integrated['dataset_source'] == 'Kaggle').sum()}")
    
    # Save integrated dataset
    print("\n[3/3] Saving integrated dataset...")
    os.makedirs("data", exist_ok=True)
    output_path = "data/integrated_data.csv"
    integrated.to_csv(output_path, index=False)
    print(f"  ✓ Saved to: {output_path}")
    
    # Print summary statistics
    print("\n" + "=" * 70)
    print("INTEGRATION SUMMARY")
    print("=" * 70)
    
    print(f"\nDataset Statistics:")
    print(f"  Total records: {len(integrated)}")
    print(f"  Total variables: {len(integrated.columns)}")
    
    print(f"\nSleep Hours:")
    print(f"  Overall mean: {integrated['sleep_hours'].mean():.2f} hours")
    print(f"  CMU mean: {integrated[integrated['dataset_source']=='CMU']['sleep_hours'].mean():.2f} hours")
    print(f"  Kaggle mean: {integrated[integrated['dataset_source']=='Kaggle']['sleep_hours'].mean():.2f} hours")
    
    print(f"\nAcademic Score (0-100):")
    print(f"  Overall mean: {integrated['academic_score'].mean():.2f}")
    print(f"  CMU mean: {integrated[integrated['dataset_source']=='CMU']['academic_score'].mean():.2f}")
    print(f"  Kaggle mean: {integrated[integrated['dataset_source']=='Kaggle']['academic_score'].mean():.2f}")
    
    print(f"\nSleep Categories:")
    print(integrated['sleep_category'].value_counts().sort_index())
    
    print(f"\nMissing Values in Common Variables:")
    common_vars = ['sleep_hours', 'academic_score', 'gender', 'age']
    for var in common_vars:
        missing = integrated[var].isna().sum()
        pct = (missing / len(integrated)) * 100
        print(f"  {var}: {missing} ({pct:.1f}%)")
    
    print("\n" + "=" * 70)
    print(f"✓ Integration complete! → {output_path}")
    print("=" * 70)

if __name__ == "__main__":
    main()
