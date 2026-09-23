"""
Data Validation Module for SuperMarketIQ Project
Author: AI Data Analytics Intern
Description: Validates enriched dataset against strict quality criteria before exploratory analysis.
"""

import os
import pandas as pd

def validate_enriched_dataset(file_path: str = os.path.join('data', 'processed', 'enriched_supermarket_data.csv')) -> bool:
    """
    Executes 10-point automated validation on processed dataset.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Enriched file not found at '{file_path}'")
    
    df = pd.read_csv(file_path)
    
    checks = {
        "Row Count (500)": len(df) == 500,
        "Column Count (24)": len(df.columns) == 24,
        "No Missing Values": df.isnull().sum().sum() == 0,
        "No Duplicate Rows": df.duplicated().sum() == 0,
        "Quantity Range (1-10)": df['Quantity'].min() == 1 and df['Quantity'].max() == 10,
        "Rating Range (3.0-5.0)": df['Rating'].min() >= 3.0 and df['Rating'].max() <= 5.0,
        "Positive Unit Price": df['Unit Price'].min() > 0,
        "Sales Calculation Exact": (abs(df['Sales'] - df['Calculated_Sales']) <= 0.01).all(),
        "Unique Invoice IDs (500)": df['Invoice ID'].nunique() == 500,
        "Valid Date Range (Jan-Jul 2026)": df['Date'].min() == '2026-01-01' and df['Date'].max() == '2026-07-01'
    }
    
    all_passed = True
    print("=" * 60)
    print("        SUPERMARKETIQ - POST-ENRICHMENT DATA VALIDATION")
    print("=" * 60)
    for check_name, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"[{status}] {check_name}")
    print("=" * 60)
    
    if all_passed:
        print("[SUCCESS] Dataset passed all 10 validation checks. Ready for EDA.")
    else:
        print("[FAILURE] Validation failed! Inspect pipeline logs.")
        
    return all_passed

if __name__ == '__main__':
    validate_enriched_dataset()
