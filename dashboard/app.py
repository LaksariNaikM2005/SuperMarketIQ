"""
SuperMarketIQ Interactive Streamlit Dashboard
File: dashboard/app.py
Author: AI Data Analytics Intern
Description: Interactive executive analytics dashboard built with Streamlit and Plotly/Matplotlib.
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(
    page_title="SuperMarketIQ - Retail Analytics Dashboard",
    page_icon="🛒",
    layout="wide"
)

@st.cache_data
def load_data():
    path = os.path.join('data', 'processed', 'enriched_supermarket_data.csv')
    if not os.path.exists(path):
        path = os.path.join('..', 'data', 'processed', 'enriched_supermarket_data.csv')
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Header
st.title("🛒 SuperMarketIQ: Executive Sales & Performance Dashboard")
st.markdown("---")

# Sidebar Filters
st.sidebar.header("🔍 Interactive Data Filters")

cities = st.sidebar.multiselect("Select City / Branch:", options=df['City'].unique(), default=df['City'].unique())
categories = st.sidebar.multiselect("Select Product Category:", options=df['Category'].unique(), default=df['Category'].unique())
cust_types = st.sidebar.multiselect("Select Customer Type:", options=df['Customer Type'].unique(), default=df['Customer Type'].unique())
payments = st.sidebar.multiselect("Select Payment Method:", options=df['Payment'].unique(), default=df['Payment'].unique())

# Filter data
filtered_df = df[
    (df['City'].isin(cities)) &
    (df['Category'].isin(categories)) &
    (df['Customer Type'].isin(cust_types)) &
    (df['Payment'].isin(payments))
]

# KPI Metric Cards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Sales Revenue", f"₹{filtered_df['Sales'].sum():,.2f}")
col2.metric("Total Transactions", f"{len(filtered_df):,}")
col3.metric("Units Sold", f"{filtered_df['Quantity'].sum():,}")
col4.metric("Avg Order Value (ATV)", f"₹{filtered_df['Sales'].mean():,.2f}" if len(filtered_df)>0 else "₹0.00")
col5.metric("Avg Rating", f"{filtered_df['Rating'].mean():.2f}/5.0" if len(filtered_df)>0 else "0.00")

st.markdown("---")

# Main Charts Grid
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    fig, ax = plt.subplots(figsize=(7, 4))
    plt.subplots_adjust(hspace=0.4)
    branch_df = filtered_df.groupby('City')['Sales'].sum().reset_index()
    sns.barplot(data=branch_df, x='City', y='Sales', palette='viridis', ax=ax)
    ax.set_title("Sales Revenue by Branch / City (INR ₹)", fontweight='bold')
    st.pyplot(fig)

with row1_col2:
    fig, ax = plt.subplots(figsize=(7, 4))
    cat_df = filtered_df.groupby('Category')['Sales'].sum().sort_values(ascending=True).reset_index()
    sns.barplot(data=cat_df, y='Category', x='Sales', palette='magma', ax=ax)
    ax.set_title("Sales Revenue by Product Category", fontweight='bold')
    st.pyplot(fig)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    fig, ax = plt.subplots(figsize=(7, 4))
    monthly_df = filtered_df.groupby(['Month', 'Month_Name'])['Sales'].sum().reset_index()
    sns.lineplot(data=monthly_df, x='Month_Name', y='Sales', marker='o', color='#2b5c8f', ax=ax)
    ax.set_title("Monthly Revenue Trend (2026)", fontweight='bold')
    st.pyplot(fig)

with row2_col2:
    fig, ax = plt.subplots(figsize=(7, 4))
    pay_df = filtered_df.groupby('Payment')['Sales'].sum()
    if len(pay_df) > 0:
        ax.pie(pay_df, labels=pay_df.index, autopct='%1.1f%%', startangle=140, colors=['#4c72b0', '#55a868', '#c44e52', '#8172b0'])
        ax.set_title("POS Payment Channel Breakdown", fontweight='bold')
    st.pyplot(fig)

st.markdown("---")

# Detailed Data Table View
st.subheader("📋 Transaction Data Table")
st.dataframe(filtered_df[['Invoice ID', 'Date', 'Branch', 'City', 'Customer Type', 'Gender', 'Product', 'Category', 'Quantity', 'Unit Price', 'Payment', 'Rating', 'Sales']].head(50))
