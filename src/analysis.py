"""
Business Analysis Module for SuperMarketIQ Project
Author: AI Data Analytics Intern
Description: Solves core business questions and exports summary tables to outputs/tables/.
"""

import os
import pandas as pd

def run_business_analysis(file_path: str = os.path.join('data', 'processed', 'enriched_supermarket_data.csv'),
                          output_dir: str = os.path.join('outputs', 'tables')) -> dict:
    """
    Executes analytical aggregations and exports summary CSV tables.
    """
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(file_path)
    
    exports = {}
    
    # Q1 & Q3: Branch & City Performance
    branch_summary = df.groupby(['Branch', 'City']).agg(
        Total_Sales=('Sales', 'sum'),
        Total_Orders=('Sales', 'count'),
        Total_Quantity=('Quantity', 'sum'),
        Average_Transaction_Value=('Sales', 'mean'),
        Average_Rating=('Rating', 'mean')
    ).reset_index().sort_values(by='Total_Sales', ascending=False)
    p1 = os.path.join(output_dir, 'branch_performance.csv')
    branch_summary.to_csv(p1, index=False)
    exports['branch_performance'] = p1
    
    # Q2 & Q8: Category Sales & Volume Performance
    category_summary = df.groupby('Category').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Quantity=('Quantity', 'sum'),
        Total_Orders=('Sales', 'count'),
        Average_Unit_Price=('Unit Price', 'mean'),
        Average_Rating=('Rating', 'mean')
    ).reset_index().sort_values(by='Total_Sales', ascending=False)
    p2 = os.path.join(output_dir, 'category_performance.csv')
    category_summary.to_csv(p2, index=False)
    exports['category_performance'] = p2
    
    # Q1 & Q7: Top & Bottom Products Performance
    product_summary = df.groupby(['Product', 'Category']).agg(
        Total_Sales=('Sales', 'sum'),
        Total_Quantity=('Quantity', 'sum'),
        Average_Unit_Price=('Unit Price', 'mean'),
        Average_Rating=('Rating', 'mean')
    ).reset_index().sort_values(by='Total_Sales', ascending=False)
    p3 = os.path.join(output_dir, 'product_performance.csv')
    product_summary.to_csv(p3, index=False)
    exports['product_performance'] = p3
    
    # Q5 & Q11: Customer Type Segment Breakdown
    customer_summary = df.groupby(['Customer Type', 'Gender']).agg(
        Total_Sales=('Sales', 'sum'),
        Total_Orders=('Sales', 'count'),
        Average_Order_Value=('Sales', 'mean'),
        Average_Rating=('Rating', 'mean')
    ).reset_index()
    p4 = os.path.join(output_dir, 'customer_segmentation.csv')
    customer_summary.to_csv(p4, index=False)
    exports['customer_segmentation'] = p4
    
    # Q6: Payment Method Breakdown
    payment_summary = df.groupby('Payment').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Orders=('Sales', 'count'),
        Average_Transaction_Value=('Sales', 'mean')
    ).reset_index().sort_values(by='Total_Sales', ascending=False)
    p5 = os.path.join(output_dir, 'payment_performance.csv')
    payment_summary.to_csv(p5, index=False)
    exports['payment_performance'] = p5
    
    # Q9: Monthly Sales Trend
    monthly_summary = df.groupby(['Year', 'Month', 'Month_Name']).agg(
        Total_Sales=('Sales', 'sum'),
        Total_Orders=('Sales', 'count'),
        Average_Order_Value=('Sales', 'mean')
    ).reset_index()
    p6 = os.path.join(output_dir, 'monthly_sales_trend.csv')
    monthly_summary.to_csv(p6, index=False)
    exports['monthly_sales_trend'] = p6

    # Q14 & Q15: Satisfaction Matrix (High Sales / Low Rating, Low Sales / High Rating)
    mean_sales = product_summary['Total_Sales'].mean()
    mean_rating = product_summary['Average_Rating'].mean()
    
    product_summary['High_Sales'] = product_summary['Total_Sales'] >= mean_sales
    product_summary['High_Rating'] = product_summary['Average_Rating'] >= mean_rating
    
    p7 = os.path.join(output_dir, 'product_satisfaction_matrix.csv')
    product_summary.to_csv(p7, index=False)
    exports['satisfaction_matrix'] = p7

    print(f"[INFO] Analysis completed. Saved {len(exports)} summary tables in '{output_dir}'")
    return exports

if __name__ == '__main__':
    run_business_analysis()
