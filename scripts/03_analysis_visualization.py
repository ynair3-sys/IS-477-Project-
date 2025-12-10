"""
Data Analysis and Visualization Script
Research Question: How do sleep patterns influence GPA and study productivity?

Author: [Your Name]
Date: December 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import json
import os

# Configuration
INPUT_FILE = "data/integrated_data.csv"
OUTPUT_DIR = "results"
FIGURES_DIR = "results/figures"
TABLES_DIR = "results/tables"

# Create output directories
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10

print("=" * 70)
print("DATA ANALYSIS: Sleep Patterns & Academic Performance")
print("=" * 70)

# Load data
print("\n[1/6] Loading integrated data...")
df = pd.read_csv(INPUT_FILE)
print(f"  Loaded {len(df)} students with {len(df.columns)} variables")

# Split by dataset
cmu_df = df[df['dataset_source'] == 'CMU'].copy()
kaggle_df = df[df['dataset_source'] == 'Kaggle'].copy()
print(f"  CMU subset: {len(cmu_df)} students")
print(f"  Kaggle subset: {len(kaggle_df)} students")

# Descriptive statistics
print("\n[2/6] Computing descriptive statistics...")

descriptive_stats = {
    "Overall": {
        "n": int(len(df)),
        "sleep_mean": float(df['sleep_hours'].mean()),
        "sleep_std": float(df['sleep_hours'].std()),
        "academic_mean": float(df['academic_score'].mean()),
        "academic_std": float(df['academic_score'].std())
    },
    "CMU": {
        "n": int(len(cmu_df)),
        "sleep_mean": float(cmu_df['sleep_hours'].mean()),
        "sleep_std": float(cmu_df['sleep_hours'].std()),
        "academic_mean": float(cmu_df['academic_score'].mean()),
        "academic_std": float(cmu_df['academic_score'].std())
    },
    "Kaggle": {
        "n": int(len(kaggle_df)),
        "sleep_mean": float(kaggle_df['sleep_hours'].mean()),
        "sleep_std": float(kaggle_df['sleep_hours'].std()),
        "academic_mean": float(kaggle_df['academic_score'].mean()),
        "academic_std": float(kaggle_df['academic_score'].std())
    }
}

sleep_dist = df['sleep_category'].value_counts().to_dict()
descriptive_stats['sleep_distribution'] = {str(k): int(v) for k, v in sleep_dist.items()}

with open(f"{TABLES_DIR}/descriptive_statistics.json", 'w') as f:
    json.dump(descriptive_stats, f, indent=2)

print("  Descriptive statistics saved")

# Correlation analysis
print("\n[3/6] Computing correlations...")

corr_all = df[['sleep_hours', 'academic_score']].corr().loc['sleep_hours', 'academic_score']
corr_cmu = cmu_df[['sleep_hours', 'academic_score']].corr().loc['sleep_hours', 'academic_score']
corr_kaggle = kaggle_df[['sleep_hours', 'academic_score']].corr().loc['sleep_hours', 'academic_score']

correlations = {
    "sleep_hours_vs_academic_score": {
        "overall": float(corr_all),
        "cmu": float(corr_cmu),
        "kaggle": float(corr_kaggle)
    }
}

if 'productivity_score' in kaggle_df.columns:
    corr_sleep_prod = kaggle_df[['sleep_hours', 'productivity_score']].corr().loc['sleep_hours', 'productivity_score']
    corr_prod_academic = kaggle_df[['productivity_score', 'academic_score']].corr().loc['productivity_score', 'academic_score']
    correlations['sleep_hours_vs_productivity'] = float(corr_sleep_prod)
    correlations['productivity_vs_academic_score'] = float(corr_prod_academic)

with open(f"{TABLES_DIR}/correlations.json", 'w') as f:
    json.dump(correlations, f, indent=2)

print("  Correlations computed and saved")

# Regression analysis
print("\n[4/6] Running regression analyses...")

results = {}

# Model 1: All students
X_all = df[['sleep_hours']].dropna()
y_all = df.loc[X_all.index, 'academic_score']

model_all = LinearRegression()
model_all.fit(X_all, y_all)
y_pred_all = model_all.predict(X_all)

results['model_1_simple'] = {
    "description": "Academic Score ~ Sleep Hours (All Students)",
    "n": int(len(X_all)),
    "coefficient": float(model_all.coef_[0]),
    "intercept": float(model_all.intercept_),
    "r_squared": float(r2_score(y_all, y_pred_all)),
    "rmse": float(np.sqrt(mean_squared_error(y_all, y_pred_all)))
}

# Model 2: CMU
X_cmu = cmu_df[['sleep_hours']].dropna()
y_cmu = cmu_df.loc[X_cmu.index, 'academic_score']

model_cmu = LinearRegression()
model_cmu.fit(X_cmu, y_cmu)
y_pred_cmu = model_cmu.predict(X_cmu)

results['model_2_cmu'] = {
    "description": "Academic Score ~ Sleep Hours (CMU Only)",
    "n": int(len(X_cmu)),
    "coefficient": float(model_cmu.coef_[0]),
    "intercept": float(model_cmu.intercept_),
    "r_squared": float(r2_score(y_cmu, y_pred_cmu)),
    "rmse": float(np.sqrt(mean_squared_error(y_cmu, y_pred_cmu)))
}

# Model 3: Kaggle
X_kaggle = kaggle_df[['sleep_hours']].dropna()
y_kaggle = kaggle_df.loc[X_kaggle.index, 'academic_score']

model_kaggle = LinearRegression()
model_kaggle.fit(X_kaggle, y_kaggle)
y_pred_kaggle = model_kaggle.predict(X_kaggle)

results['model_3_kaggle'] = {
    "description": "Academic Score ~ Sleep Hours (Kaggle Only)",
    "n": int(len(X_kaggle)),
    "coefficient": float(model_kaggle.coef_[0]),
    "intercept": float(model_kaggle.intercept_),
    "r_squared": float(r2_score(y_kaggle, y_pred_kaggle)),
    "rmse": float(np.sqrt(mean_squared_error(y_kaggle, y_pred_kaggle)))
}

# Model 4: Mediation
if 'productivity_score' in kaggle_df.columns:
    X_a = kaggle_df[['sleep_hours']].dropna()
    y_a = kaggle_df.loc[X_a.index, 'productivity_score'].dropna()
    X_a = X_a.loc[y_a.index]
    
    model_a = LinearRegression()
    model_a.fit(X_a, y_a)
    path_a = float(model_a.coef_[0])
    
    X_b = kaggle_df[['sleep_hours', 'productivity_score']].dropna()
    y_b = kaggle_df.loc[X_b.index, 'academic_score']
    
    model_b = LinearRegression()
    model_b.fit(X_b, y_b)
    path_b = float(model_b.coef_[1])
    path_c_prime = float(model_b.coef_[0])
    path_c = float(model_kaggle.coef_[0])
    
    indirect_effect = path_a * path_b
    proportion_mediated = (indirect_effect / path_c) if path_c != 0 else 0
    
    results['model_4_mediation'] = {
        "description": "Mediation: Sleep -> Productivity -> Academic Score",
        "n": int(len(X_b)),
        "path_a_sleep_to_productivity": path_a,
        "path_b_productivity_to_academic": path_b,
        "path_c_total_effect": path_c,
        "path_c_prime_direct_effect": path_c_prime,
        "indirect_effect": indirect_effect,
        "proportion_mediated": float(proportion_mediated)
    }

with open(f"{TABLES_DIR}/regression_results.json", 'w') as f:
    json.dump(results, f, indent=2)

print("  Regression analyses completed and saved")

# Sleep category analysis
print("\n[5/6] Analyzing sleep categories...")

sleep_categories = df['sleep_category'].dropna().unique()
groups = [df[df['sleep_category'] == cat]['academic_score'].dropna() for cat in sleep_categories]
f_stat, p_value = stats.f_oneway(*groups)

category_analysis = {
    "anova": {
        "f_statistic": float(f_stat),
        "p_value": float(p_value),
        "significant": bool(p_value < 0.05)
    },
    "by_category": {}
}

for cat in sleep_categories:
    subset = df[df['sleep_category'] == cat]
    category_analysis["by_category"][str(cat)] = {
        "n": int(len(subset)),
        "academic_score_mean": float(subset['academic_score'].mean()),
        "academic_score_std": float(subset['academic_score'].std())
    }

with open(f"{TABLES_DIR}/category_analysis.json", 'w') as f:
    json.dump(category_analysis, f, indent=2)

print("  Category analysis completed and saved")

# Visualizations
print("\n[6/6] Creating visualizations...")

# Figure 1: Sleep distribution
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].hist(df['sleep_hours'], bins=25, color='steelblue', edgecolor='black', alpha=0.7)
axes[0].axvline(df['sleep_hours'].mean(), color='red', linestyle='--', linewidth=2, 
                label=f"Mean: {df['sleep_hours'].mean():.2f}h")
axes[0].axvline(7, color='green', linestyle=':', linewidth=2, label='Recommended: 7h')
axes[0].set_xlabel('Sleep Hours per Night')
axes[0].set_ylabel('Number of Students')
axes[0].set_title('Distribution of Sleep Duration')
axes[0].legend()
axes[0].grid(alpha=0.3)

cat_counts = df['sleep_category'].value_counts().sort_index()
colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4']
axes[1].bar(range(len(cat_counts)), cat_counts.values, color=colors, edgecolor='black', alpha=0.8)
axes[1].set_xticks(range(len(cat_counts)))
axes[1].set_xticklabels(cat_counts.index, rotation=0)
axes[1].set_ylabel('Number of Students')
axes[1].set_title('Sleep Quality Categories')
axes[1].grid(alpha=0.3, axis='y')

for i, v in enumerate(cat_counts.values):
    axes[1].text(i, v + 15, f'{v}\n({v/len(df)*100:.1f}%)', ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(f"{FIGURES_DIR}/01_sleep_distribution.png", dpi=300, bbox_inches='tight')
plt.close()

print("  Figure 1 saved: 01_sleep_distribution.png")

# Figure 2: Sleep vs performance
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].scatter(df['sleep_hours'], df['academic_score'], alpha=0.3, s=30, color='steelblue')
X_plot = np.linspace(df['sleep_hours'].min(), df['sleep_hours'].max(), 100).reshape(-1, 1)
y_plot = model_all.predict(X_plot)
axes[0].plot(X_plot, y_plot, 'r-', linewidth=2, 
            label=f'y = {model_all.coef_[0]:.2f}x + {model_all.intercept_:.2f}\nR² = {r2_score(y_all, y_pred_all):.3f}')
axes[0].set_xlabel('Sleep Hours per Night')
axes[0].set_ylabel('Academic Score (0-100)')
axes[0].set_title('Sleep Duration vs Academic Performance\n(All Students)')
axes[0].legend()
axes[0].grid(alpha=0.3)

df_clean = df.dropna(subset=['sleep_category', 'academic_score'])
cat_order = ['Poor', 'Insufficient', 'Adequate', 'Optimal']
sns.boxplot(data=df_clean, x='sleep_category', y='academic_score', 
            palette=colors, order=cat_order, ax=axes[1])
axes[1].set_xlabel('Sleep Category')
axes[1].set_ylabel('Academic Score (0-100)')
axes[1].set_title('Academic Performance by Sleep Category')
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f"{FIGURES_DIR}/02_sleep_vs_performance.png", dpi=300, bbox_inches='tight')
plt.close()

print("  Figure 2 saved: 02_sleep_vs_performance.png")

# Figure 3: Dataset comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

data_sleep = [cmu_df['sleep_hours'], kaggle_df['sleep_hours']]
bp1 = axes[0].boxplot(data_sleep, labels=['CMU\n(Fitbit)', 'Kaggle\n(Self-report)'],
                      patch_artist=True, showmeans=True)
for patch, color in zip(bp1['boxes'], ['lightblue', 'lightcoral']):
    patch.set_facecolor(color)
axes[0].set_ylabel('Sleep Hours per Night')
axes[0].set_title('Sleep Duration by Dataset')
axes[0].grid(alpha=0.3, axis='y')

data_academic = [cmu_df['academic_score'], kaggle_df['academic_score']]
bp2 = axes[1].boxplot(data_academic, labels=['CMU\n(GPA scaled)', 'Kaggle\n(Exam scores)'],
                      patch_artist=True, showmeans=True)
for patch, color in zip(bp2['boxes'], ['lightblue', 'lightcoral']):
    patch.set_facecolor(color)
axes[1].set_ylabel('Academic Score (0-100)')
axes[1].set_title('Academic Performance by Dataset')
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f"{FIGURES_DIR}/03_dataset_comparison.png", dpi=300, bbox_inches='tight')
plt.close()

print("  Figure 3 saved: 03_dataset_comparison.png")

# Figure 4: Productivity mediation
if 'productivity_score' in kaggle_df.columns:
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    axes[0, 0].scatter(kaggle_df['sleep_hours'], kaggle_df['productivity_score'], 
                      alpha=0.3, s=30, color='green')
    axes[0, 0].set_xlabel('Sleep Hours')
    axes[0, 0].set_ylabel('Productivity Score')
    axes[0, 0].set_title(f'Sleep to Productivity\nr = {corr_sleep_prod:.3f}')
    axes[0, 0].grid(alpha=0.3)
    
    axes[0, 1].scatter(kaggle_df['productivity_score'], kaggle_df['academic_score'], 
                      alpha=0.3, s=30, color='purple')
    axes[0, 1].set_xlabel('Productivity Score')
    axes[0, 1].set_ylabel('Academic Score')
    axes[0, 1].set_title(f'Productivity to Academic\nr = {corr_prod_academic:.3f}')
    axes[0, 1].grid(alpha=0.3)
    
    if 'study_hours_per_day' in kaggle_df.columns:
        study_by_sleep = kaggle_df.groupby('sleep_category')['study_hours_per_day'].mean()
        axes[1, 0].bar(range(len(study_by_sleep)), study_by_sleep.values, 
                      color=colors[:len(study_by_sleep)], edgecolor='black', alpha=0.8)
        axes[1, 0].set_xticks(range(len(study_by_sleep)))
        axes[1, 0].set_xticklabels(study_by_sleep.index, rotation=0)
        axes[1, 0].set_ylabel('Study Hours per Day')
        axes[1, 0].set_title('Study Hours by Sleep Category')
        axes[1, 0].grid(alpha=0.3, axis='y')
    
    if 'attendance_percentage' in kaggle_df.columns:
        attend_by_sleep = kaggle_df.groupby('sleep_category')['attendance_percentage'].mean()
        axes[1, 1].bar(range(len(attend_by_sleep)), attend_by_sleep.values, 
                      color=colors[:len(attend_by_sleep)], edgecolor='black', alpha=0.8)
        axes[1, 1].set_xticks(range(len(attend_by_sleep)))
        axes[1, 1].set_xticklabels(attend_by_sleep.index, rotation=0)
        axes[1, 1].set_ylabel('Attendance Percentage')
        axes[1, 1].set_title('Attendance by Sleep Category')
        axes[1, 1].grid(alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/04_productivity_mediation.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("  Figure 4 saved: 04_productivity_mediation.png")

# Summary
print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
print(f"\nKey Findings:")
print(f"  Overall sleep-performance correlation: r = {corr_all:.3f}")
print(f"  Each hour of sleep -> {model_all.coef_[0]:.2f} points increase")
print(f"  {(df['sleep_category'].isin(['Poor', 'Insufficient'])).sum()} students ({(df['sleep_category'].isin(['Poor', 'Insufficient'])).sum()/len(df)*100:.1f}%) sleep deprived")

if 'model_4_mediation' in results:
    print(f"  Productivity mediates {results['model_4_mediation']['proportion_mediated']*100:.1f}% of sleep effect")

print(f"\nOutputs saved to:")
print(f"  Tables: {TABLES_DIR}/")
print(f"  Figures: {FIGURES_DIR}/")
print("\n" + "=" * 70)
