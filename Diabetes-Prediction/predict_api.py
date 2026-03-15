#!/usr/bin/env python3
"""
Diabetes Prediction API Script
Loads the actual CareSync Streamlit pipeline model (model.pkl) and predicts.
Inputs: pregnancies, glucose, bmi, age, insulin
Outputs: JSON { prediction: 0|1, probability: float }
"""
import sys
import json
import numpy as np
import os
import warnings
from pathlib import Path

# Suppress sklearn version warnings
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')
warnings.filterwarnings('ignore', message='.*sklearn.*')

def load_model():
  try:
    import joblib
    # model.pkl is stored at the project root of Diabetes-Prediction
    model_path = Path(__file__).parent / 'model.pkl'
    if not model_path.exists():
      raise FileNotFoundError(f"Model file not found: {model_path}")
    
    # Suppress warnings when loading the model
    with warnings.catch_warnings():
      warnings.simplefilter("ignore")
      model = joblib.load(str(model_path))
    return model
  except Exception as e:
    print(f"Error loading model.pkl: {e}", file=sys.stderr)
    return None

def predict_diabetes(pregnancies, glucose, bmi, age, insulin=0.0):
  try:
    import pandas as pd
    model = load_model()
    if model is None:
      raise Exception("Failed to load model.pkl")

    # The saved pipeline expects a DataFrame with these columns
    df = pd.DataFrame([[pregnancies, glucose, insulin, bmi, age]],
              columns=['Pregnancies','Glucose','Insulin','BMI','Age'])

    # Suppress warnings during prediction
    with warnings.catch_warnings():
      warnings.simplefilter("ignore")
      proba = float(model.predict_proba(df)[:, 1][0])
      pred = int(1 if proba >= 0.32 else 0)  # Use same threshold as Streamlit config

    return { 'prediction': pred, 'probability': proba }
  except Exception as e:
    return { 'error': str(e), 'prediction': 0, 'probability': 0.0 }

def main():
  try:
    if len(sys.argv) != 6:
      print("Usage: python predict_api.py <pregnancies> <glucose> <bmi> <age> <insulin>", file=sys.stderr)
      sys.exit(1)

    pregnancies = int(float(sys.argv[1]))
    glucose = float(sys.argv[2])
    bmi = float(sys.argv[3])
    age = int(float(sys.argv[4]))
    insulin = float(sys.argv[5])

    result = predict_diabetes(pregnancies, glucose, bmi, age, insulin)
    print(json.dumps(result))
  except Exception as e:
    print(json.dumps({ 'error': str(e), 'prediction': 0, 'probability': 0.0 }))
    sys.exit(1)

if __name__ == '__main__':
  main()
