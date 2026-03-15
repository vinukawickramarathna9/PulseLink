import pandas as pd
import joblib
from PIL import Image
from data.config import thresholds
import os



from sklearn.metrics import (accuracy_score,
                             precision_score,
                             recall_score,
                             f1_score,
                             roc_auc_score)

# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, 'datasets', 'diabetes.csv')
data = pd.read_csv(data_path)
X = data[['Pregnancies', 'Glucose', 'Insulin', 'BMI', 'Age']]
y = data['Outcome']

page_icon = Image.open(os.path.join(current_dir, "image", "page_icon.jpeg"))

model = joblib.load(os.path.join(current_dir, 'model.pkl'))



y_score = model.predict_proba(X)[:, 1]
y_pred = (y_score >= thresholds).astype(int)

# Accuracy Score
accuracy_result = round(accuracy_score(y, y_pred) * 100, 2)
# F1 Score
f1_result = round(f1_score(y, y_pred) * 100, 2)
# Recall Score
recall_result = round(recall_score(y, y_pred) * 100, 2)
# Precision Score
precision_result = round(precision_score(y, y_pred) * 100, 2)
# ROC AUC Score
roc_auc = round(roc_auc_score(y, y_score) * 100, 2)