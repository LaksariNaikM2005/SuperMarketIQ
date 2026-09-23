"""
Feature Engineering Module for SuperMarketIQ Project
Author: AI Data Analytics Intern
Description: Enriches cleaned supermarket data with temporal, monetary, and categorical binned attributes.
"""

import os
import pandas as pd

def enrich_supermarket_data(cleaned_df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches cleaned DataFrame with meaningful business features.
    
    Derived Features:
    1. Year: Temporal year (2026)
    2. Month: Month number (1-7)
    3. Month_Name: Full month name ('January', etc.)
    4. Day: Day of month (1-31)
    5. Day_Name: Day of week ('Monday', etc.)
    6. Quarter: Fiscal quarter ('Q1', 'Q2', 'Q3')
    7. Is_Weekend: Binary flag (1 = Weekend, 0 = Weekday)
    8. Calculated_Sales: Re-computed Quantity * Unit Price rounded to 2 decimals
    9. Order_Value_Category: Order spend tier ('Low (<200)', 'Medium (200-600)', 'High (>600)')
    10. Price_Category: Item price tier ('Budget (<50)', 'Mid-Range (50-150)', 'Premium (>150)')
    11. Quantity_Category: Unit volume tier ('Small (1-3)', 'Medium (4-7)', 'Bulk (8-10)')
    
    Returns:
    --------
    pd.DataFrame
        Enriched DataFrame with 23 features.
    """
    df = cleaned_df.copy()
    
    # Ensure Date column is datetime64
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 1. Temporal Features
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Month_Name'] = df['Date'].dt.strftime('%B')
    df['Day'] = df['Date'].dt.day
    df['Day_Name'] = df['Date'].dt.day_name()
    df['Quarter'] = 'Q' + df['Date'].dt.quarter.astype(str)
    df['Is_Weekend'] = df['Date'].dt.dayofweek.apply(lambda x: 1 if x >= 5 else 0)
    
    # 2. Calculated Sales Audit Field
    df['Calculated_Sales'] = (df['Quantity'] * df['Unit Price']).round(2)
    
    # 3. Spend Tier Binning
    df['Order_Value_Category'] = pd.cut(
        df['Sales'],
        bins=[0, 200, 600, 10000],
        labels=['Low (<200)', 'Medium (200-600)', 'High (>600)']
    ).astype(str)
    
    # 4. Pricing Tier Binning
    df['Price_Category'] = pd.cut(
        df['Unit Price'],
        bins=[0, 50, 150, 1000],
        labels=['Budget (<50)', 'Mid-Range (50-150)', 'Premium (>150)']
    ).astype(str)
    
    # 5. Quantity Volume Binning
    df['Quantity_Category'] = pd.cut(
        df['Quantity'],
        bins=[0, 3, 7, 10],
        labels=['Small (1-3)', 'Medium (4-7)', 'Bulk (8-10)']
    ).astype(str)
    
    print(f"[INFO] Data enrichment complete. Original cols: {cleaned_df.shape[1]} -> Enriched cols: {df.shape[1]}")
    return df

def save_enriched_data(df: pd.DataFrame, processed_dir: str = os.path.join('data', 'processed')) -> dict:
    """
    Saves enriched DataFrame to CSV and Excel formats in data/processed/.
    """
    os.makedirs(processed_dir, exist_ok=True)
    
    csv_path = os.path.join(processed_dir, 'enriched_supermarket_data.csv')
    xlsx_path = os.path.join(processed_dir, 'enriched_supermarket_data.xlsx')
    
    df.to_csv(csv_path, index=False)
    df.to_excel(xlsx_path, index=False)
    
    print(f"[INFO] Enriched dataset saved to '{csv_path}' and '{xlsx_path}'")
    return {'csv_path': csv_path, 'xlsx_path': xlsx_path}

if __name__ == '__main__':
    clean_path = os.path.join('data', 'processed', 'cleaned_supermarket_data.csv')
    cleaned_df = pd.read_csv(clean_path)
    enriched_df = enrich_supermarket_data(cleaned_df)
    save_enriched_data(enriched_df)
