"""
Inference module for making predictions with trained model
"""
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import warnings

warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')


class DiabetesPredictor:
    """
    Wrapper class for diabetes prediction using trained model.
    """
    
    def __init__(self, model_path=None, threshold=0.32):
        """
        Initialize predictor with trained model.
        
        Args:
            model_path (str): Path to trained model file
            threshold (float): Classification threshold (default: 0.32)
        """
        if model_path is None:
            project_root = Path(__file__).parent.parent.parent
            model_path = project_root / 'models' / 'model.pkl'
        
        self.model_path = model_path
        self.threshold = threshold
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained model from disk."""
        if not Path(self.model_path).exists():
            raise FileNotFoundError(f"Model not found at: {self.model_path}")
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.model = joblib.load(str(self.model_path))
    
    def predict(self, pregnancies, glucose, bmi, age, insulin=0.0):
        """
        Predict diabetes risk for a single patient.
        
        Args:
            pregnancies (int): Number of pregnancies
            glucose (float): Plasma glucose concentration
            bmi (float): Body mass index
            age (int): Age in years
            insulin (float): Insulin level (default: 0.0)
            
        Returns:
            dict: {
                'prediction': int (0 or 1),
                'probability': float,
                'risk_level': str
            }
        """
        # Validate inputs
        self._validate_inputs(pregnancies, glucose, bmi, age, insulin)
        
        # Create DataFrame
        df = pd.DataFrame([[pregnancies, glucose, insulin, bmi, age]],
                         columns=['Pregnancies', 'Glucose', 'Insulin', 'BMI', 'Age'])
        
        # Make prediction
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            probability = float(self.model.predict_proba(df)[:, 1][0])
            prediction = int(1 if probability >= self.threshold else 0)
        
        # Determine risk level
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return {
            'prediction': prediction,
            'probability': round(probability, 4),
            'risk_level': risk_level
        }
    
    def predict_batch(self, data_df):
        """
        Predict diabetes risk for multiple patients.
        
        Args:
            data_df (pd.DataFrame): DataFrame with columns 
                                   ['Pregnancies', 'Glucose', 'Insulin', 'BMI', 'Age']
            
        Returns:
            pd.DataFrame: Original data with predictions added
        """
        required_columns = ['Pregnancies', 'Glucose', 'Insulin', 'BMI', 'Age']
        
        if not all(col in data_df.columns for col in required_columns):
            raise ValueError(f"DataFrame must contain columns: {required_columns}")
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            probabilities = self.model.predict_proba(data_df[required_columns])[:, 1]
            predictions = (probabilities >= self.threshold).astype(int)
        
        result_df = data_df.copy()
        result_df['probability'] = probabilities
        result_df['prediction'] = predictions
        
        return result_df
    
    @staticmethod
    def _validate_inputs(pregnancies, glucose, bmi, age, insulin):
        """Validate input ranges."""
        if not (0 <= pregnancies <= 20):
            raise ValueError("Pregnancies must be between 0 and 20")
        if not (0 <= glucose <= 300):
            raise ValueError("Glucose must be between 0 and 300")
        if not (10 <= bmi <= 70):
            raise ValueError("BMI must be between 10 and 70")
        if not (1 <= age <= 120):
            raise ValueError("Age must be between 1 and 120")
        if not (0 <= insulin <= 1000):
            raise ValueError("Insulin must be between 0 and 1000")
