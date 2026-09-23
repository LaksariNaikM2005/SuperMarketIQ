"""
Data Loading Module for SuperMarketIQ Project
Author: AI Data Analytics Intern
Description: Handles reading raw Excel datasets, structural validation, and basic summary metrics.
"""

import os
import pandas as pd

def load_raw_data(file_path: str = os.path.join('data', 'raw', 'SUPER MARKET DATA.xlsx')) -> pd.DataFrame:
    """
    Loads raw supermarket dataset from specified Excel file path.
    
    Parameters:
    -----------
    file_path : str
        Relative or absolute path to SUPER MARKET DATA.xlsx
        
    Returns:
    --------
    pd.DataFrame
        Loaded raw DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw dataset file not found at path: {file_path}")
    
    df = pd.read_excel(file_path)
    print(f"[INFO] Data loaded successfully from '{file_path}'. Shape: {df.shape}")
    return df

def get_structural_summary(df: pd.DataFrame) -> dict:
    """
    Generates a dictionary summary of row count, column count, null count, duplicate count, and date range.
    """
    summary = {
        'num_rows': df.shape[0],
        'num_cols': df.shape[1],
        'columns': list(df.columns),
        'missing_values_total': int(df.isnull().sum().sum()),
        'duplicate_rows': int(df.duplicated().sum()),
        'date_min': str(df['Date'].min()) if 'Date' in df.columns else None,
        'date_max': str(df['Date'].max()) if 'Date' in df.columns else None
    }
    return summary

if __name__ == '__main__':
    data = load_raw_data()
    summary = get_structural_summary(data)
    print("[SUMMARY]", summary)
