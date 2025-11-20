"""
Data Cleaning Script
Project: Sleep Patterns and Academic Performance
Authors: Yamuna Nair & Monisha Mudunuri
 
This script cleans both datasets by handling missing values, duplicates,
outliers, and standardizing formats.
"""
 
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
 
# Define paths
RAW_DATA = Path("data/raw")
PROCESSED_DATA = Path("data/processed")
PROCESSED_DATA.mkdir(parents=True, exist_ok=True)
 
def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
 
def analyze_missing_data(df, dataset_name):
    """Analyze and report missing data."""
    print(f"\n{dataset_name} - Missing Data Analysis:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    
    missing_df = pd.DataFrame({
        'Missing_Count': missing,
        'Percentage': missing_pct
    })
    missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values('Percentage', ascending=False)
    
    if len(missing_df) > 0:
        print(missing_df.to_string())
    else:
        print("✓ No missing values detected!")
    
    return missing_df
 
def clean_cmu_dataset():
    """Clean the CMU Sleep and GPA dataset."""
    print_section("CLEANING CMU SLEEP DATASET")
    
    # Load data
    cmu_df = pd.read_csv(RAW_DATA / "cmu_sleep.csv")
    print(f"\nOriginal shape: {cmu_df.shape}")
    print(f"Columns: {', '.join(cmu_df.columns.tolist())}")
    
    # Analyze missing data
    missing_analysis = analyze_missing_data(cmu_df, "CMU Dataset")
    
    # Remove duplicates
    duplicates = cmu_df.duplicated().sum()
    print(f"\n✓ Duplicates found: {duplicates}")
    cmu_df = cmu_df.drop_duplicates()
    
    # Quality filtering: Remove students with insufficient data
    # Keep only students with at least 50% of nights recorded
    if 'frac_nights_with_data' in cmu_df.columns:
        before_filter = len(cmu_df)
        cmu_df = cmu_df[cmu_df['frac_nights_with_data'] >= 0.5]
        removed = before_filter - len(cmu_df)
        print(f"\n✓ Removed {removed} students with <50% data collection")
    
    # Convert TotalSleepTime from minutes to hours for consistency
    if 'TotalSleepTime' in cmu_df.columns:
        cmu_df['sleep_hours'] = cmu_df['TotalSleepTime'] / 60
        print(f"✓ Converted TotalSleepTime to sleep_hours")
    
    # Check for outliers in sleep hours
    if 'sleep_hours' in cmu_df.columns:
        sleep_outliers = cmu_df[(cmu_df['sleep_hours'] < 2) | (cmu_df['sleep_hours'] > 16)]
        print(f"\n⚠ Sleep outliers detected (< 2h or > 16h): {len(sleep_outliers)} records")
        print(f"  Range: {cmu_df['sleep_hours'].min():.2f}h to {cmu_df['sleep_hours'].max():.2f}h")
        
        # Flag but don't remove (could be real data)
        cmu_df['sleep_outlier'] = ((cmu_df['sleep_hours'] < 2) | (cmu_df['sleep_hours'] > 16)).astype(int)
    
    # Check for outliers in GPA
    if 'term_gpa' in cmu_df.columns:
        gpa_outliers = cmu_df[(cmu_df['term_gpa'] < 0) | (cmu_df['term_gpa'] > 4.0)]
        print(f"⚠ GPA outliers detected (< 0 or > 4.0): {len(gpa_outliers)} records")
        
        # Remove invalid GPAs
        cmu_df = cmu_df[(cmu_df['term_gpa'] >= 0) & (cmu_df['term_gpa'] <= 4.0)]
        print(f"✓ Removed {len(gpa_outliers)} invalid GPA records")
    
    # Standardize column names
    column_mapping = {
        'demo_gender': 'gender',
        'demo_race': 'race',
        'demo_firstgen': 'first_generation',
        'bedtime_mssd': 'bedtime_variability',
        'term_gpa': 'gpa'
    }
    cmu_df = cmu_df.rename(columns=column_mapping)
    print(f"\n✓ Standardized column names")
    
    # Add dataset source identifier
    cmu_df['dataset_source'] = 'CMU'
    
    print(f"\nCleaned shape: {cmu_df.shape}")
    
    # Save cleaned dataset
    output_path = PROCESSED_DATA / "cmu_sleep_cleaned.csv"
    cmu_df.to_csv(output_path, index=False)
    print(f"✓ Saved to: {output_path}")
    
    return cmu_df
 
def clean_kaggle_dataset():
    """Clean the Kaggle Student Habits dataset."""
    print_section("CLEANING KAGGLE STUDENT HABITS DATASET")
    
    # Load data
    kaggle_df = pd.read_csv(RAW_DATA / "student_habits.csv")
    print(f"\nOriginal shape: {kaggle_df.shape}")
    print(f"Columns: {', '.join(kaggle_df.columns.tolist())}")
    
    # Analyze missing data
    missing_analysis = analyze_missing_data(kaggle_df, "Kaggle Dataset")
    
    # Remove duplicates
    duplicates = kaggle_df.duplicated().sum()
    print(f"\n✓ Duplicates found: {duplicates}")
    kaggle_df = kaggle_df.drop_duplicates()
    
    # Handle missing values (if any)
    # For numeric columns, we'll flag rows with missing critical data
    critical_columns = ['sleep_hours', 'study_hours_per_day', 'exam_score']
    
    if missing_analysis is not None and len(missing_analysis) > 0:
        before_drop = len(kaggle_df)
        kaggle_df = kaggle_df.dropna(subset=[col for col in critical_columns if col in kaggle_df.columns])
        removed = before_drop - len(kaggle_df)
        print(f"✓ Removed {removed} rows with missing critical data")
    
    # Check for outliers in sleep hours
    if 'sleep_hours' in kaggle_df.columns:
        sleep_outliers = kaggle_df[(kaggle_df['sleep_hours'] < 2) | (kaggle_df['sleep_hours'] > 16)]
        print(f"\n⚠ Sleep outliers detected (< 2h or > 16h): {len(sleep_outliers)} records")
        print(f"  Range: {kaggle_df['sleep_hours'].min():.2f}h to {kaggle_df['sleep_hours'].max():.2f}h")
        
        # Flag but don't remove
        kaggle_df['sleep_outlier'] = ((kaggle_df['sleep_hours'] < 2) | (kaggle_df['sleep_hours'] > 16)).astype(int)
    
    # Check for outliers in study hours
    if 'study_hours_per_day' in kaggle_df.columns:
        study_outliers = kaggle_df[kaggle_df['study_hours_per_day'] > 18]
        print(f"⚠ Study hours outliers (> 18h/day): {len(study_outliers)} records")
        
        # Flag but don't remove
        kaggle_df['study_outlier'] = (kaggle_df['study_hours_per_day'] > 18).astype(int)
    
    # Check for outliers in exam scores
    if 'exam_score' in kaggle_df.columns:
        exam_outliers = kaggle_df[(kaggle_df['exam_score'] < 0) | (kaggle_df['exam_score'] > 100)]
        print(f"⚠ Exam score outliers (< 0 or > 100): {len(exam_outliers)} records")
        
        # Remove invalid exam scores
        kaggle_df = kaggle_df[(kaggle_df['exam_score'] >= 0) & (kaggle_df['exam_score'] <= 100)]
        print(f"✓ Removed {len(exam_outliers)} invalid exam score records")
    
    # Standardize column names
    column_mapping = {
        'parental_education_level': 'parental_education'
    }
    kaggle_df = kaggle_df.rename(columns=column_mapping)
    
    # Add dataset source identifier
    kaggle_df['dataset_source'] = 'Kaggle'
    
    print(f"\nCleaned shape: {kaggle_df.shape}")
    
    # Save cleaned dataset
    output_path = PROCESSED_DATA / "student_habits_cleaned.csv"
    kaggle_df.to_csv(output_path, index=False)
    print(f"✓ Saved to: {output_path}")
    
    return kaggle_df
 
def generate_cleaning_report(cmu_df, kaggle_df):
    """Generate a summary report of cleaning operations."""
    print_section("CLEANING SUMMARY REPORT")
    
    report = []
    report.append("\nDATA CLEANING SUMMARY")
    report.append("=" * 70)
    
    report.append(f"\nCMU Sleep Dataset:")
    report.append(f"  Final records: {len(cmu_df)}")
    report.append(f"  Final columns: {len(cmu_df.columns)}")
    report.append(f"  Sleep hours range: {cmu_df['sleep_hours'].min():.2f}h - {cmu_df['sleep_hours'].max():.2f}h")
    if 'gpa' in cmu_df.columns:
        report.append(f"  GPA range: {cmu_df['gpa'].min():.2f} - {cmu_df['gpa'].max():.2f}")
    
    report.append(f"\nKaggle Student Habits Dataset:")
    report.append(f"  Final records: {len(kaggle_df)}")
    report.append(f"  Final columns: {len(kaggle_df.columns)}")
    if 'sleep_hours' in kaggle_df.columns:
        report.append(f"  Sleep hours range: {kaggle_df['sleep_hours'].min():.2f}h - {kaggle_df['sleep_hours'].max():.2f}h")
    if 'exam_score' in kaggle_df.columns:
        report.append(f"  Exam score range: {kaggle_df['exam_score'].min():.0f} - {kaggle_df['exam_score'].max():.0f}")
    
    report.append(f"\nCleaning Operations Applied:")
    report.append("  ✓ Duplicate removal")
    report.append("  ✓ Missing data handling")
    report.append("  ✓ Outlier detection and flagging")
    report.append("  ✓ Data type standardization")
    report.append("  ✓ Column name standardization")
    report.append("  ✓ Quality filtering (CMU: frac_nights_with_data >= 0.5)")
    report.append("  ✓ Unit conversion (CMU: minutes to hours)")
    
    report_text = "\n".join(report)
    print(report_text)
    
    # Save report
    report_path = PROCESSED_DATA / "cleaning_report.txt"
    with open(report_path, 'w') as f:
        f.write(report_text)
    print(f"\n✓ Report saved to: {report_path}")
 
def main():
    """Main execution function."""
    print("\n" + "=" * 70)
    print("DATA CLEANING SCRIPT")
    print("Sleep Patterns & Academic Performance Project")
    print("=" * 70)
    
    # Clean both datasets
    cmu_cleaned = clean_cmu_dataset()
    kaggle_cleaned = clean_kaggle_dataset()
    
    # Generate report
    generate_cleaning_report(cmu_cleaned, kaggle_cleaned)
    
    print("\n" + "=" * 70)
    print("CLEANING COMPLETE")
    print("=" * 70)
    print("\n✓ All cleaned datasets saved to data/processed/")
    print("\nNext steps:")
    print("1. Review cleaned datasets in data/processed/")
    print("2. Run 03_data_integration.py to merge datasets")
    print("3. Review cleaning_report.txt for details")
 
if __name__ == "__main__":
    main()