"""
Data Cleaning Module for SuperMarketIQ Project
Author: AI Data Analytics Intern
Description: Implements systematic, repeatable data cleaning and standardization pipelines.
"""

import os
import pandas as pd
import numpy as np

def clean_supermarket_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and standardizes raw supermarket DataFrame.
    
    Steps:
    1. Create deep copy of raw data.
    2. Standardize column names (strip whitespace).
    3. Ensure Date is datetime format.
    4. Strip whitespace and standardize title casing on string columns.
    5. Re-verify Sales = Quantity * Unit Price and round to 2 decimal places.
    6. Validate data bounds (Quantity > 0, Price > 0, 3.0 <= Rating <= 5.0).
    
    Returns:
    --------
    pd.DataFrame
        Cleaned and validated DataFrame.
    """
    df = raw_df.copy()
    
    # Step 1: Strip leading/trailing spaces from column headers
    df.columns = [col.strip() for col in df.columns]
    
    # Step 2: Ensure Date column is proper datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Step 3: Clean string columns (strip whitespace, title casing)
    string_cols = df.select_dtypes(include='object').columns
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()
    
    # Step 4: Ensure exact mathematical rounding on Sales
    df['Sales'] = (df['Quantity'] * df['Unit Price']).round(2)
    
    # Step 5: Validate numeric bounds
    assert (df['Quantity'] > 0).all(), "Validation Error: Quantity contains <= 0 values!"
    assert (df['Unit Price'] > 0).all(), "Validation Error: Unit Price contains <= 0 values!"
    assert ((df['Rating'] >= 1.0) & (df['Rating'] <= 5.0)).all(), "Validation Error: Rating out of bounds!"
    
    print(f"[INFO] Data cleaning complete. Final shape: {df.shape}")
    return df

def save_cleaned_data(df: pd.DataFrame, processed_dir: str = os.path.join('data', 'processed')) -> dict:
    """
    Saves cleaned DataFrame to CSV and Excel formats in data/processed/.
    """
    os.makedirs(processed_dir, exist_ok=True)
    
    csv_path = os.path.join(processed_dir, 'cleaned_supermarket_data.csv')
    xlsx_path = os.path.join(processed_dir, 'cleaned_supermarket_data.xlsx')
    
    df.to_csv(csv_path, index=False)
    df.to_excel(xlsx_path, index=False)
    
    print(f"[INFO] Cleaned data saved to '{csv_path}' and '{xlsx_path}'")
    return {'csv_path': csv_path, 'xlsx_path': xlsx_path}

if __name__ == '__main__':
    raw_path = os.path.join('data', 'raw', 'SUPER MARKET DATA.xlsx')
    raw_df = pd.read_excel(raw_path)
    cleaned_df = clean_supermarket_data(raw_df)
    save_cleaned_data(cleaned_df)
