"""
Configuration settings for diabetes prediction model
"""

# Model configuration
MODEL_CONFIG = {
    'model_type': 'RandomForestClassifier',
    'hyperparameters': {
        'max_depth': 6,
        'n_estimators': 300,
        'criterion': 'entropy',
        'random_state': 42
    },
    'threshold': 0.32,  # Optimized for medical context (high recall)
}

# Feature configuration
FEATURE_CONFIG = {
    'input_features': ['Pregnancies', 'Glucose', 'Insulin', 'BMI', 'Age'],
    'selected_features': [
        'Pregnancies', 'Glucose', 'BMI', 'PregnancyRatio',
        'RiskScore', 'InsulinEfficiency', 'Glucose_BMI', 'BMI_Age',
        'Glucose_woe', 'RiskScore_woe'
    ]
}

# Data validation ranges
VALIDATION_RANGES = {
    'Pregnancies': (0, 20),
    'Glucose': (0, 300),
    'BMI': (10, 70),
    'Age': (1, 120),
    'Insulin': (0, 1000)
}

# Path configuration (relative to project root)
PATH_CONFIG = {
    'data_dir': 'datasets',
    'model_dir': 'models',
    'notebook_dir': 'notebooks',
}
