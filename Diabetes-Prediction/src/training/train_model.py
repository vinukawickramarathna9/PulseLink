"""
Model training and pipeline construction
"""
import joblib
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
from pathlib import Path

from src.preprocessing.transformers import FeatureEngineering, WoEEncoding, ColumnSelector


def build_pipeline():
    """
    Constructs the complete ML pipeline with preprocessing and model.
    
    Returns:
        sklearn.pipeline.Pipeline: Complete ML pipeline
    """
    selected_columns = [
        'Pregnancies', 'Glucose', 'BMI', 'PregnancyRatio',
        'RiskScore', 'InsulinEfficiency', 'Glucose_BMI', 'BMI_Age',
        'Glucose_woe', 'RiskScore_woe'
    ]

    # Pipeline with tuned hyperparameters
    pipeline = Pipeline([
        ('feature_engineering', FeatureEngineering()),
        ('woe_encoding', WoEEncoding()),
        ('column_selector', ColumnSelector(selected_columns)),
        ('model', RandomForestClassifier(
            max_depth=6,
            n_estimators=300,
            criterion='entropy',
            random_state=42
        ))
    ])
    
    return pipeline


def train_model(data_path=None, save_path=None):
    """
    Trains the diabetes prediction model and saves it.
    
    Args:
        data_path (str): Path to training data CSV
        save_path (str): Path to save trained model
        
    Returns:
        tuple: (trained_pipeline, metrics_dict)
    """
    # Set default paths
    if data_path is None:
        project_root = Path(__file__).parent.parent.parent
        data_path = project_root / 'datasets' / 'diabetes.csv'
    
    if save_path is None:
        project_root = Path(__file__).parent.parent.parent
        save_path = project_root / 'models' / 'model.pkl'
    
    # Load data
    data = pd.read_csv(data_path)
    X = data[['Pregnancies', 'Glucose', 'Insulin', 'BMI', 'Age']]
    y = data['Outcome']
    
    # Build and train pipeline
    pipeline = build_pipeline()
    pipeline.fit(X, y)
    
    # Evaluate
    y_pred_proba = pipeline.predict_proba(X)[:, 1]
    y_pred = (y_pred_proba >= 0.32).astype(int)
    
    roc_auc = roc_auc_score(y, y_pred_proba)
    
    metrics = {
        'roc_auc_score': round(roc_auc * 100, 2),
        'classification_report': classification_report(y, y_pred),
        'confusion_matrix': confusion_matrix(y, y_pred).tolist()
    }
    
    # Save model
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump(pipeline, save_path)
    
    print(f"Model trained successfully!")
    print(f"ROC AUC Score: {metrics['roc_auc_score']}%")
    print(f"Model saved to: {save_path}")
    
    return pipeline, metrics


if __name__ == '__main__':
    train_model()
