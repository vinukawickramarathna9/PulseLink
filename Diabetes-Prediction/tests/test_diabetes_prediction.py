"""
Comprehensive test suite for diabetes prediction model

This test file demonstrates:
- Data validation tests
- Model prediction sanity tests
- Error handling tests
- Edge case testing

Run with: pytest tests/test_diabetes_prediction.py -v
"""
import pytest
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.preprocessing.transformers import FeatureEngineering, WoEEncoding, ColumnSelector
from src.inference.predict import DiabetesPredictor
from src.training.train_model import build_pipeline
from config.config import VALIDATION_RANGES, MODEL_CONFIG


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_data():
    """Provide sample valid input data."""
    return pd.DataFrame({
        'Pregnancies': [6, 1, 8],
        'Glucose': [148, 85, 183],
        'Insulin': [0, 0, 0],
        'BMI': [33.6, 26.6, 23.3],
        'Age': [50, 31, 32]
    })


@pytest.fixture
def sample_labels():
    """Provide sample labels."""
    return np.array([1, 0, 1])


@pytest.fixture
def predictor():
    """Initialize predictor (skips if model doesn't exist)."""
    model_path = project_root / 'models' / 'model.pkl'
    if not model_path.exists():
        pytest.skip("Model file not found. Train model first.")
    return DiabetesPredictor(model_path=model_path)


# ============================================================================
# DATA VALIDATION TESTS
# ============================================================================

class TestDataValidation:
    """Test suite for data validation and preprocessing."""
    
    def test_input_data_shape(self, sample_data):
        """Test that input data has correct shape and columns."""
        required_columns = ['Pregnancies', 'Glucose', 'Insulin', 'BMI', 'Age']
        assert all(col in sample_data.columns for col in required_columns), \
            "Missing required columns"
        assert len(sample_data) > 0, "Empty dataset"
    
    def test_data_types(self, sample_data):
        """Test that data types are numeric."""
        for col in sample_data.columns:
            assert pd.api.types.is_numeric_dtype(sample_data[col]), \
                f"Column {col} is not numeric"
    
    def test_no_missing_values(self, sample_data):
        """Test that there are no missing values in critical columns."""
        assert not sample_data.isnull().any().any(), \
            "Dataset contains missing values"
    
    def test_value_ranges(self, sample_data):
        """Test that values are within expected ranges."""
        for feature, (min_val, max_val) in VALIDATION_RANGES.items():
            if feature in sample_data.columns:
                assert sample_data[feature].min() >= min_val, \
                    f"{feature} has values below minimum ({min_val})"
                assert sample_data[feature].max() <= max_val, \
                    f"{feature} has values above maximum ({max_val})"
    
    def test_glucose_sanity(self, sample_data):
        """Test glucose values are physiologically reasonable."""
        # Glucose < 40 is hypoglycemia, > 250 is severe hyperglycemia
        assert sample_data['Glucose'].between(40, 250).any(), \
            "Glucose values may be unrealistic"
    
    def test_bmi_sanity(self, sample_data):
        """Test BMI values are reasonable."""
        # Typical BMI range is 15-50
        assert sample_data['BMI'].between(15, 50).all(), \
            "BMI values outside typical range"


# ============================================================================
# PREPROCESSING TESTS
# ============================================================================

class TestPreprocessing:
    """Test suite for preprocessing transformers."""
    
    def test_feature_engineering_creates_features(self, sample_data):
        """Test that FeatureEngineering creates expected features."""
        fe = FeatureEngineering()
        transformed = fe.fit_transform(sample_data)
        
        expected_features = [
            'PregnancyRatio', 'RiskScore', 'InsulinEfficiency', 
            'Glucose_BMI', 'BMI_Age'
        ]
        
        for feature in expected_features:
            assert feature in transformed.columns, \
                f"Missing engineered feature: {feature}"
    
    def test_feature_engineering_no_inf(self, sample_data):
        """Test that FeatureEngineering doesn't produce infinite values."""
        fe = FeatureEngineering()
        transformed = fe.fit_transform(sample_data)
        
        assert not np.isinf(transformed.values).any(), \
            "Infinite values produced during feature engineering"
    
    def test_woe_encoding_fit_transform(self, sample_data, sample_labels):
        """Test WoE encoding fit and transform."""
        woe = WoEEncoding()
        woe.fit(sample_data, sample_labels)
        transformed = woe.transform(sample_data)
        
        # Check that WoE columns are created
        woe_columns = [col for col in transformed.columns if col.endswith('_woe')]
        assert len(woe_columns) > 0, "No WoE columns created"
    
    def test_column_selector(self, sample_data):
        """Test ColumnSelector filters columns correctly."""
        fe = FeatureEngineering()
        transformed = fe.fit_transform(sample_data)
        
        selected_cols = ['Pregnancies', 'Glucose', 'BMI']
        cs = ColumnSelector(selected_cols)
        result = cs.transform(transformed)
        
        assert list(result.columns) == selected_cols, \
            "ColumnSelector didn't select correct columns"


# ============================================================================
# MODEL PREDICTION TESTS
# ============================================================================

class TestModelPredictions:
    """Test suite for model prediction functionality."""
    
    def test_predictor_initialization(self, predictor):
        """Test that predictor initializes correctly."""
        assert predictor.model is not None, "Model not loaded"
        assert predictor.threshold == MODEL_CONFIG['threshold'], \
            "Threshold mismatch"
    
    def test_single_prediction_format(self, predictor):
        """Test that single prediction returns correct format."""
        result = predictor.predict(
            pregnancies=6, 
            glucose=148, 
            bmi=33.6, 
            age=50, 
            insulin=0
        )
        
        assert 'prediction' in result, "Missing 'prediction' key"
        assert 'probability' in result, "Missing 'probability' key"
        assert 'risk_level' in result, "Missing 'risk_level' key"
        assert result['prediction'] in [0, 1], "Invalid prediction value"
        assert 0 <= result['probability'] <= 1, "Probability out of range"
    
    def test_prediction_probabilities_valid(self, predictor):
        """Test that prediction probabilities are valid."""
        result = predictor.predict(
            pregnancies=6, 
            glucose=148, 
            bmi=33.6, 
            age=50
        )
        
        assert isinstance(result['probability'], float), \
            "Probability is not float"
        assert 0 <= result['probability'] <= 1, \
            "Probability not in [0, 1] range"
    
    def test_risk_level_classification(self, predictor):
        """Test that risk levels are correctly classified."""
        # Low risk case
        result_low = predictor.predict(
            pregnancies=1, 
            glucose=85, 
            bmi=26.6, 
            age=31
        )
        
        # High risk case
        result_high = predictor.predict(
            pregnancies=10, 
            glucose=200, 
            bmi=45, 
            age=60
        )
        
        assert result_low['risk_level'] in ['Low', 'Medium', 'High']
        assert result_high['risk_level'] in ['Low', 'Medium', 'High']
    
    def test_batch_prediction(self, predictor, sample_data):
        """Test batch prediction functionality."""
        result_df = predictor.predict_batch(sample_data)
        
        assert 'prediction' in result_df.columns, \
            "Batch prediction missing 'prediction' column"
        assert 'probability' in result_df.columns, \
            "Batch prediction missing 'probability' column"
        assert len(result_df) == len(sample_data), \
            "Batch prediction returned wrong number of results"
    
    def test_prediction_consistency(self, predictor):
        """Test that same inputs produce same outputs."""
        inputs = {
            'pregnancies': 6,
            'glucose': 148,
            'bmi': 33.6,
            'age': 50,
            'insulin': 0
        }
        
        result1 = predictor.predict(**inputs)
        result2 = predictor.predict(**inputs)
        
        assert result1['prediction'] == result2['prediction'], \
            "Predictions not consistent"
        assert abs(result1['probability'] - result2['probability']) < 1e-6, \
            "Probabilities not consistent"


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

class TestErrorHandling:
    """Test suite for error handling and edge cases."""
    
    def test_invalid_pregnancies(self, predictor):
        """Test that invalid pregnancies raise error."""
        with pytest.raises(ValueError):
            predictor.predict(
                pregnancies=-1,  # Invalid
                glucose=100,
                bmi=25,
                age=30
            )
    
    def test_invalid_glucose(self, predictor):
        """Test that invalid glucose raises error."""
        with pytest.raises(ValueError):
            predictor.predict(
                pregnancies=2,
                glucose=500,  # Invalid (too high)
                bmi=25,
                age=30
            )
    
    def test_invalid_bmi(self, predictor):
        """Test that invalid BMI raises error."""
        with pytest.raises(ValueError):
            predictor.predict(
                pregnancies=2,
                glucose=100,
                bmi=5,  # Invalid (too low)
                age=30
            )
    
    def test_invalid_age(self, predictor):
        """Test that invalid age raises error."""
        with pytest.raises(ValueError):
            predictor.predict(
                pregnancies=2,
                glucose=100,
                bmi=25,
                age=0  # Invalid
            )
    
    def test_invalid_insulin(self, predictor):
        """Test that invalid insulin raises error."""
        with pytest.raises(ValueError):
            predictor.predict(
                pregnancies=2,
                glucose=100,
                bmi=25,
                age=30,
                insulin=2000  # Invalid (too high)
            )
    
    def test_missing_columns_batch(self, predictor):
        """Test that missing columns in batch prediction raise error."""
        incomplete_data = pd.DataFrame({
            'Pregnancies': [6],
            'Glucose': [148]
            # Missing other required columns
        })
        
        with pytest.raises(ValueError):
            predictor.predict_batch(incomplete_data)
    
    def test_model_file_not_found(self):
        """Test that missing model file raises appropriate error."""
        with pytest.raises(FileNotFoundError):
            DiabetesPredictor(model_path='nonexistent_model.pkl')


# ============================================================================
# PIPELINE INTEGRATION TESTS
# ============================================================================

class TestPipelineIntegration:
    """Test suite for end-to-end pipeline functionality."""
    
    def test_pipeline_builds_successfully(self):
        """Test that pipeline can be constructed."""
        pipeline = build_pipeline()
        assert pipeline is not None, "Pipeline construction failed"
        assert hasattr(pipeline, 'fit'), "Pipeline missing fit method"
        assert hasattr(pipeline, 'predict'), "Pipeline missing predict method"
    
    def test_pipeline_fit_predict(self, sample_data, sample_labels):
        """Test that pipeline can fit and predict."""
        pipeline = build_pipeline()
        
        # Fit
        pipeline.fit(sample_data, sample_labels)
        
        # Predict
        predictions = pipeline.predict(sample_data)
        assert len(predictions) == len(sample_data), \
            "Wrong number of predictions"
        assert all(p in [0, 1] for p in predictions), \
            "Invalid prediction values"


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""
    
    def test_zero_pregnancies(self, predictor):
        """Test prediction with zero pregnancies."""
        result = predictor.predict(
            pregnancies=0,
            glucose=100,
            bmi=25,
            age=25
        )
        assert result['prediction'] in [0, 1]
    
    def test_maximum_values(self, predictor):
        """Test prediction with maximum valid values."""
        result = predictor.predict(
            pregnancies=20,
            glucose=300,
            bmi=70,
            age=120,
            insulin=1000
        )
        assert result['prediction'] in [0, 1]
    
    def test_minimum_values(self, predictor):
        """Test prediction with minimum valid values."""
        result = predictor.predict(
            pregnancies=0,
            glucose=0,
            bmi=10,
            age=1,
            insulin=0
        )
        assert result['prediction'] in [0, 1]
    
    def test_typical_healthy_person(self, predictor):
        """Test prediction for typical healthy person."""
        result = predictor.predict(
            pregnancies=2,
            glucose=90,
            bmi=22,
            age=30,
            insulin=80
        )
        # Healthy person should have low probability
        assert result['probability'] < 0.5, \
            "Healthy person classified as high risk"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
