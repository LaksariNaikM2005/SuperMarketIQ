"""
Visualization Module for SuperMarketIQ Project
Author: AI Data Analytics Intern
Description: Generates publication-ready charts and exports PNG figures to outputs/charts/.
"""

import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def generate_all_charts(df: pd.DataFrame, output_dir: str = os.path.join('outputs', 'charts')) -> list:
    """
    Generates 10 executive-level data visualization charts.
    """
    os.makedirs(output_dir, exist_ok=True)
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 10
    
    generated_files = []
    
    # Palette definition
    primary_color = '#1f77b4'
    palette = sns.color_palette("muted")
    
    # -------------------------------------------------------------
    # Chart 1: Total Sales by Branch & City
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5))
    branch_df = df.groupby(['Branch', 'City'])['Sales'].sum().reset_index()
    sns.barplot(data=branch_df, x='City', y='Sales', palette='viridis', ax=ax)
    ax.set_title('Total Sales Revenue by Branch & City (INR)', fontsize=14, fontweight='bold')
    ax.set_xlabel('City (Branch)', fontsize=12)
    ax.set_ylabel('Total Sales (INR ₹)', fontsize=12)
    for p in ax.patches:
        ax.annotate(f'₹{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                    ha='center', va='center', fontsize=11, color='white', fontweight='bold')
    path1 = os.path.join(output_dir, '01_sales_by_branch_city.png')
    plt.tight_layout()
    plt.savefig(path1, dpi=300)
    plt.close()
    generated_files.append(path1)
    
    # -------------------------------------------------------------
    # Chart 2: Total Sales by Product Category
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    cat_df = df.groupby('Category')['Sales'].sum().sort_values(ascending=True).reset_index()
    sns.barplot(data=cat_df, y='Category', x='Sales', palette='magma', ax=ax)
    ax.set_title('Product Category Sales Performance (INR)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Total Revenue (INR ₹)', fontsize=12)
    ax.set_ylabel('Product Category', fontsize=12)
    for p in ax.patches:
        ax.annotate(f' ₹{p.get_width():,.0f}', (p.get_width(), p.get_y() + p.get_height()/2.),
                    va='center', fontsize=10, fontweight='bold')
    path2 = os.path.join(output_dir, '02_sales_by_category.png')
    plt.tight_layout()
    plt.savefig(path2, dpi=300)
    plt.close()
    generated_files.append(path2)
    
    # -------------------------------------------------------------
    # Chart 3: Monthly Revenue Trend
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_df = df.groupby(['Year', 'Month', 'Month_Name'])['Sales'].sum().reset_index()
    sns.lineplot(data=monthly_df, x='Month_Name', y='Sales', marker='o', linewidth=2.5, color='#2b5c8f', ax=ax)
    ax.set_title('Monthly Revenue Performance (Jan 2026 - Jul 2026)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Sales Revenue (INR ₹)', fontsize=12)
    for x, y in zip(monthly_df['Month_Name'], monthly_df['Sales']):
        ax.annotate(f'₹{y:,.0f}', (x, y + 1000), ha='center', fontsize=10, fontweight='bold')
    path3 = os.path.join(output_dir, '03_monthly_sales_trend.png')
    plt.tight_layout()
    plt.savefig(path3, dpi=300)
    plt.close()
    generated_files.append(path3)
    
    # -------------------------------------------------------------
    # Chart 4: Payment Channel Distribution (Donut Chart)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7, 7))
    pay_df = df.groupby('Payment')['Sales'].sum()
    colors = ['#4c72b0', '#55a868', '#c44e52', '#8172b0']
    wedges, texts, autotexts = ax.pie(pay_df, labels=pay_df.index, autopct='%1.1f%%', startangle=140,
                                      colors=colors, wedgeprops=dict(width=0.4, edgecolor='w'))
    plt.setp(autotexts, size=11, weight="bold", color="white")
    ax.set_title('Sales Distribution by POS Payment Channel', fontsize=14, fontweight='bold')
    path4 = os.path.join(output_dir, '04_payment_channel_distribution.png')
    plt.tight_layout()
    plt.savefig(path4, dpi=300)
    plt.close()
    generated_files.append(path4)
    
    # -------------------------------------------------------------
    # Chart 5: Customer Type Average Transaction Value (ATV)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5))
    cust_df = df.groupby(['Customer Type', 'Gender'])['Sales'].mean().reset_index()
    sns.barplot(data=cust_df, x='Customer Type', y='Sales', hue='Gender', palette='Set2', ax=ax)
    ax.set_title('Average Order Value (ATV) by Customer Type & Gender', fontsize=14, fontweight='bold')
    ax.set_ylabel('Average Transaction Value (INR ₹)', fontsize=12)
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f'₹{p.get_height():,.2f}', (p.get_x() + p.get_width()/2., p.get_height()/2),
                        ha='center', va='center', fontsize=10, color='white', fontweight='bold')
    path5 = os.path.join(output_dir, '05_customer_type_atv_comparison.png')
    plt.tight_layout()
    plt.savefig(path5, dpi=300)
    plt.close()
    generated_files.append(path5)
    
    # -------------------------------------------------------------
    # Chart 6: Customer Rating Distribution
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df['Rating'], bins=10, kde=True, color='#2b83ba', ax=ax)
    ax.set_title('Customer Satisfaction Rating Distribution (3.0 to 5.0)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Rating Score', fontsize=12)
    ax.set_ylabel('Frequency (Transactions)', fontsize=12)
    path6 = os.path.join(output_dir, '06_rating_distribution.png')
    plt.tight_layout()
    plt.savefig(path6, dpi=300)
    plt.close()
    generated_files.append(path6)
    
    # -------------------------------------------------------------
    # Chart 7: Unit Price vs Sales Scatter Plot
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='Unit Price', y='Sales', hue='Category', style='Customer Type',
                    s=80, alpha=0.8, ax=ax)
    ax.set_title('Unit Price vs Total Order Sales by Category', fontsize=14, fontweight='bold')
    ax.set_xlabel('Unit Price (INR ₹)', fontsize=12)
    ax.set_ylabel('Total Sales (INR ₹)', fontsize=12)
    path7 = os.path.join(output_dir, '07_unit_price_vs_sales_scatter.png')
    plt.tight_layout()
    plt.savefig(path7, dpi=300)
    plt.close()
    generated_files.append(path7)
    
    # -------------------------------------------------------------
    # Chart 8: Top 5 & Bottom 5 Products Revenue
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    prod_rev = df.groupby('Product')['Sales'].sum().sort_values(ascending=False)
    
    top5 = prod_rev.head(5).reset_index()
    sns.barplot(data=top5, x='Sales', y='Product', palette='crest', ax=ax1)
    ax1.set_title('Top 5 Products by Revenue', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Sales (INR ₹)')
    
    bot5 = prod_rev.tail(5).reset_index()
    sns.barplot(data=bot5, x='Sales', y='Product', palette='flare', ax=ax2)
    ax2.set_title('Bottom 5 Products by Revenue', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Sales (INR ₹)')
    
    path8 = os.path.join(output_dir, '08_top_bottom_products.png')
    plt.tight_layout()
    plt.savefig(path8, dpi=300)
    plt.close()
    generated_files.append(path8)

    # -------------------------------------------------------------
    # Chart 9: Heatmap Correlation Matrix
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6))
    num_cols = ['Quantity', 'Unit Price', 'Rating', 'Sales']
    sns.heatmap(df[num_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
    ax.set_title('Correlation Heatmap Matrix', fontsize=14, fontweight='bold')
    path9 = os.path.join(output_dir, '09_correlation_heatmap.png')
    plt.tight_layout()
    plt.savefig(path9, dpi=300)
    plt.close()
    generated_files.append(path9)

    print(f"[INFO] Successfully generated {len(generated_files)} executive charts in '{output_dir}'")
    return generated_files

if __name__ == '__main__':
    data_path = os.path.join('data', 'processed', 'enriched_supermarket_data.csv')
    df = pd.read_csv(data_path)
    generate_all_charts(df)
