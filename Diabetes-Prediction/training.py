import joblib
import pandas as pd
import os
from sklearn.metrics import roc_auc_score
from function.model import Model

# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, 'datasets', 'diabetes.csv')
data = pd.read_csv(data_path)
X = data[['Pregnancies', 'Glucose', 'Insulin', 'BMI', 'Age']]
y = data['Outcome']


Model.fit(X, y)

y_pred = Model.predict_proba(X)[:, 1]

print("ROC_AUC Score: ", (roc_auc_score(y, y_pred) * 100).round(2))

model_path = os.path.join(current_dir, 'model.pkl')
joblib.dump(Model, model_path)