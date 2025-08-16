#!/usr/bin/env python3
"""
Palmer Penguins Dataset - Exploratory Data Analysis
===================================================

This script performs comprehensive exploratory data analysis on the Palmer Penguins dataset,
examining the structure, quality, and key characteristics of the data.

Dataset: Palmer Penguins from Palmer Archipelago, Antarctica
Variables: Species, island, bill measurements, flipper length, body mass, sex, year
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set display options for better output
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print("=" * 80)
print("PALMER PENGUINS DATASET - EXPLORATORY DATA ANALYSIS")
print("=" * 80)
print(f"Analysis performed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Load the dataset
print("1. LOADING DATASET")
print("-" * 40)
try:
    df = pd.read_csv('penguins.csv')
    print(f"✓ Dataset loaded successfully")
    print(f"✓ Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print()
except Exception as e:
    print(f"✗ Error loading dataset: {e}")
    exit(1)

# Dataset structure and basic information
print("2. DATASET STRUCTURE")
print("-" * 40)
print("Column names and data types:")
print(df.dtypes)
print()

print("First 5 rows:")
print(df.head())
print()

print("Last 5 rows:")
print(df.tail())
print()

# Missing values analysis
print("3. MISSING VALUES ANALYSIS")
print("-" * 40)
missing_counts = df.isnull().sum()
missing_percentages = (df.isnull().sum() / len(df)) * 100

missing_summary = pd.DataFrame({
    'Missing Count': missing_counts,
    'Missing Percentage': missing_percentages
})

print("Missing values by column:")
print(missing_summary)
print()

if missing_counts.sum() > 0:
    print("Rows with any missing values:")
    rows_with_missing = df[df.isnull().any(axis=1)]
    print(f"Total rows with missing data: {len(rows_with_missing)}")
    print("\nSample rows with missing values:")
    print(rows_with_missing.head(10))
    print()
else:
    print("✓ No missing values found in the dataset")
    print()

# Categorical variables analysis
print("4. CATEGORICAL VARIABLES ANALYSIS")
print("-" * 40)

categorical_columns = df.select_dtypes(include=['object']).columns
print(f"Categorical columns: {list(categorical_columns)}")
print()

for col in categorical_columns:
    print(f"{col.upper()} - Value counts:")
    value_counts = df[col].value_counts(dropna=False)
    print(value_counts)
    print(f"Unique values: {df[col].nunique()}")
    print()

# Numerical variables analysis
print("5. NUMERICAL VARIABLES ANALYSIS")
print("-" * 40)

numerical_columns = df.select_dtypes(include=[np.number]).columns
print(f"Numerical columns: {list(numerical_columns)}")
print()

print("Descriptive statistics for numerical variables:")
print(df[numerical_columns].describe())
print()

# Detailed statistics for each numerical variable
for col in numerical_columns:
    print(f"{col.upper()} - Detailed statistics:")
    series = df[col].dropna()
    
    stats = {
        'Count': len(series),
        'Mean': series.mean(),
        'Median': series.median(),
        'Mode': series.mode().iloc[0] if not series.mode().empty else 'No mode',
        'Standard Deviation': series.std(),
        'Variance': series.var(),
        'Skewness': series.skew(),
        'Kurtosis': series.kurtosis(),
        'Min': series.min(),
        'Max': series.max(),
        'Range': series.max() - series.min(),
        'Q1 (25%)': series.quantile(0.25),
        'Q3 (75%)': series.quantile(0.75),
        'IQR': series.quantile(0.75) - series.quantile(0.25)
    }
    
    for stat, value in stats.items():
        if isinstance(value, (int, float)) and stat != 'Count':
            print(f"  {stat}: {value:.2f}")
        else:
            print(f"  {stat}: {value}")
    print()

# Outlier detection using IQR method
print("6. OUTLIER DETECTION")
print("-" * 40)

for col in numerical_columns:
    series = df[col].dropna()
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = series[(series < lower_bound) | (series > upper_bound)]
    
    print(f"{col.upper()}:")
    print(f"  IQR bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
    print(f"  Number of outliers: {len(outliers)}")
    if len(outliers) > 0:
        print(f"  Outlier values: {sorted(outliers.values)}")
    print()

# Correlation analysis
print("7. CORRELATION ANALYSIS")
print("-" * 40)

correlation_matrix = df[numerical_columns].corr()
print("Correlation matrix:")
print(correlation_matrix.round(3))
print()

# Find strongest correlations
correlations = []
for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        col1 = correlation_matrix.columns[i]
        col2 = correlation_matrix.columns[j]
        corr_value = correlation_matrix.iloc[i, j]
        correlations.append((col1, col2, corr_value))

correlations.sort(key=lambda x: abs(x[2]), reverse=True)

print("Strongest correlations (absolute value):")
for col1, col2, corr in correlations[:5]:
    print(f"  {col1} ↔ {col2}: {corr:.3f}")
print()

# Species-specific analysis
print("8. SPECIES-SPECIFIC ANALYSIS")
print("-" * 40)

if 'species' in df.columns:
    species_counts = df['species'].value_counts()
    print("Species distribution:")
    print(species_counts)
    print()
    
    print("Average measurements by species:")
    species_stats = df.groupby('species')[numerical_columns].mean()
    print(species_stats.round(2))
    print()
    
    print("Standard deviation by species:")
    species_std = df.groupby('species')[numerical_columns].std()
    print(species_std.round(2))
    print()

# Island analysis
print("9. ISLAND ANALYSIS")
print("-" * 40)

if 'island' in df.columns:
    island_counts = df['island'].value_counts()
    print("Island distribution:")
    print(island_counts)
    print()
    
    if 'species' in df.columns:
        print("Species by island:")
        species_island = pd.crosstab(df['species'], df['island'])
        print(species_island)
        print()

# Sex analysis
print("10. SEX ANALYSIS")
print("-" * 40)

if 'sex' in df.columns:
    sex_counts = df['sex'].value_counts(dropna=False)
    print("Sex distribution:")
    print(sex_counts)
    print()
    
    if 'species' in df.columns:
        print("Sex distribution by species:")
        sex_species = pd.crosstab(df['species'], df['sex'], dropna=False)
        print(sex_species)
        print()
    
    # Sexual dimorphism analysis
    print("Average measurements by sex:")
    sex_stats = df.groupby('sex')[numerical_columns].mean()
    print(sex_stats.round(2))
    print()

# Data quality assessment
print("11. DATA QUALITY ASSESSMENT")
print("-" * 40)

total_cells = df.shape[0] * df.shape[1]
missing_cells = df.isnull().sum().sum()
completeness = ((total_cells - missing_cells) / total_cells) * 100

print(f"Overall data completeness: {completeness:.1f}%")
print(f"Total observations: {df.shape[0]}")
print(f"Complete observations (no missing values): {df.dropna().shape[0]}")
print()

# Identify potential data issues
print("Potential data quality issues:")
issues = []

# Check for duplicate rows
duplicates = df.duplicated().sum()
if duplicates > 0:
    issues.append(f"• {duplicates} duplicate rows found")

# Check for impossible values (negative measurements)
for col in numerical_columns:
    if 'mm' in col or 'mass' in col:
        negative_values = (df[col] < 0).sum()
        if negative_values > 0:
            issues.append(f"• {negative_values} negative values in {col}")

# Check for extremely high values that might be data entry errors
for col in numerical_columns:
    series = df[col].dropna()
    if len(series) > 0:
        Q3 = series.quantile(0.75)
        extreme_threshold = Q3 * 3  # Values 3x the Q3 might be suspicious
        extreme_values = (series > extreme_threshold).sum()
        if extreme_values > 0:
            issues.append(f"• {extreme_values} extremely high values in {col} (>{extreme_threshold:.1f})")

if issues:
    for issue in issues:
        print(issue)
else:
    print("✓ No obvious data quality issues detected")

print()

# Summary and recommendations
print("12. SUMMARY AND RECOMMENDATIONS")
print("-" * 40)

print("KEY FINDINGS:")
print("• Dataset contains biological measurements of penguins from Palmer Archipelago")
print(f"• {df.shape[0]} observations across {df.shape[1]} variables")
print(f"• {df['species'].nunique() if 'species' in df.columns else 'Unknown'} penguin species represented")
print(f"• Data completeness: {completeness:.1f}%")

if missing_counts.sum() > 0:
    print(f"• Missing data present in {(missing_counts > 0).sum()} columns")

print()
print("ANALYTICAL OPPORTUNITIES:")
print("• Species comparison: Examine morphological differences between species")
print("• Sexual dimorphism: Investigate size differences between males and females")
print("• Island effects: Analyze whether geographic location affects measurements")
print("• Allometric relationships: Study how different body measurements scale together")
print("• Classification modeling: Predict species based on physical measurements")

print()
print("RECOMMENDED VISUALIZATIONS:")
print("• Box plots comparing measurements across species")
print("• Scatter plots showing relationships between measurements")
print("• Histograms showing distribution shapes for each measurement")
print("• Correlation heatmap for numerical variables")
print("• Violin plots showing distribution differences by sex and species")

print()
print("DATA CLEANING RECOMMENDATIONS:")
if missing_counts.sum() > 0:
    print("• Decide on strategy for missing values (imputation vs. removal)")
    print("• Investigate patterns in missing data")
else:
    print("• No missing data issues to address")

if len([issue for issue in issues if 'duplicate' in issue]) > 0:
    print("• Remove or investigate duplicate rows")

print("• Verify outliers are legitimate measurements rather than data entry errors")

print()
print("ANALYSIS COMPLETE")
print("=" * 80)