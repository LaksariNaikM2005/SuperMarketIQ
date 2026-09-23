"""
Machine Learning & Target Leakage Educational Module for SuperMarketIQ
Author: AI Data Analytics Intern
Description: Demonstrates supervised classification (Logistic Regression), model evaluation metrics, and target leakage prevention.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report

def train_basket_value_classifier(file_path: str = os.path.join('data', 'processed', 'enriched_supermarket_data.csv')) -> dict:
    """
    Trains a Logistic Regression model to predict High-Value Orders (Sales > 500).
    Demonstrates model training, evaluation metrics, and target leakage analysis.
    """
    df = pd.read_csv(file_path)
    
    # 1. Define Target: High Value Order (1 if Sales > 500 else 0)
    df['Is_High_Value_Order'] = (df['Sales'] > 500).astype(int)
    
    # 2. Define Features WITHOUT Direct Target Leakage (Excluding raw Sales / Calculated_Sales)
    feature_cols = ['Quantity', 'Unit Price', 'Rating', 'Customer Type', 'Gender', 'Branch', 'Payment', 'Category']
    X = pd.get_dummies(df[feature_cols], drop_first=True)
    y = df['Is_High_Value_Order']
    
    # 3. Train-Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 4. Train Model
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Predict & Evaluate
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred)),
        'recall': float(recall_score(y_test, y_pred)),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
        'feature_importance': dict(zip(X.columns, model.coef_[0].round(4)))
    }
    
    print("=" * 60)
    print("      SUPERMARKETIQ - LOGISTIC REGRESSION CLASSIFIER")
    print("=" * 60)
    print(f"Target: Is_High_Value_Order (Sales > 500)")
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print("\nConfusion Matrix:")
    print(np.array(metrics['confusion_matrix']))
    print("=" * 60)
    
    return metrics

if __name__ == '__main__':
    train_basket_value_classifier()
