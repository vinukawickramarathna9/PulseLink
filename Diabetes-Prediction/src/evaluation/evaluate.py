"""
Model evaluation utilities
"""
import pandas as pd
import numpy as np
from sklearn.metrics import (
    roc_auc_score, accuracy_score, precision_score, 
    recall_score, f1_score, confusion_matrix, classification_report
)
from pathlib import Path
import json


def evaluate_model(model, X, y, threshold=0.32):
    """
    Evaluate model performance on given data.
    
    Args:
        model: Trained sklearn pipeline
        X (pd.DataFrame): Features
        y (array-like): True labels
        threshold (float): Classification threshold
        
    Returns:
        dict: Dictionary of evaluation metrics
    """
    # Get predictions
    y_pred_proba = model.predict_proba(X)[:, 1]
    y_pred = (y_pred_proba >= threshold).astype(int)
    
    # Calculate metrics
    metrics = {
        'roc_auc': round(roc_auc_score(y, y_pred_proba), 4),
        'accuracy': round(accuracy_score(y, y_pred), 4),
        'precision': round(precision_score(y, y_pred), 4),
        'recall': round(recall_score(y, y_pred), 4),
        'f1_score': round(f1_score(y, y_pred), 4),
        'confusion_matrix': confusion_matrix(y, y_pred).tolist(),
        'threshold': threshold
    }
    
    return metrics


def generate_metrics_report(metrics, save_path=None):
    """
    Generate a human-readable metrics report.
    
    Args:
        metrics (dict): Metrics dictionary from evaluate_model
        save_path (str, optional): Path to save JSON report
        
    Returns:
        str: Formatted report string
    """
    report = f"""
Model Performance Report
========================
Threshold: {metrics['threshold']}
ROC AUC Score: {metrics['roc_auc']*100:.2f}%
Accuracy: {metrics['accuracy']*100:.2f}%
Precision: {metrics['precision']*100:.2f}%
Recall: {metrics['recall']*100:.2f}%
F1 Score: {metrics['f1_score']*100:.2f}%

Confusion Matrix:
{np.array(metrics['confusion_matrix'])}

Interpretation:
- High recall is prioritized in medical contexts to minimize false negatives
- Threshold of {metrics['threshold']} balances precision and recall
- ROC AUC indicates overall model discriminative ability
"""
    
    if save_path:
        with open(save_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"Metrics saved to: {save_path}")
    
    return report


if __name__ == '__main__':
    # Example usage
    import joblib
    
    project_root = Path(__file__).parent.parent.parent
    model_path = project_root / 'models' / 'model.pkl'
    data_path = project_root / 'datasets' / 'diabetes.csv'
    
    if model_path.exists() and data_path.exists():
        model = joblib.load(model_path)
        data = pd.read_csv(data_path)
        
        X = data[['Pregnancies', 'Glucose', 'Insulin', 'BMI', 'Age']]
        y = data['Outcome']
        
        metrics = evaluate_model(model, X, y)
        report = generate_metrics_report(metrics)
        print(report)
