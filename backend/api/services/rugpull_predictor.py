import joblib
import numpy as np
import os
import xgboost as xgb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Load model and preprocessors

MODEL_PATH = os.path.join(BASE_DIR, "xgboost_rugpull.pkl")
IMPUTER_PATH = os.path.join(BASE_DIR, "imputer.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

model = joblib.load(MODEL_PATH)
imputer = joblib.load(IMPUTER_PATH)
scaler = joblib.load(SCALER_PATH)

def predict_rugpull(features):
    """
    Given a feature array, preprocess and predict rugpull probability.
    """
    # Ensure features are in a NumPy array
    features = np.array(features).reshape(1, -1)

    # Apply preprocessing (Impute missing values, scale)
    features_imputed = imputer.transform(features)
    features_scaled = scaler.transform(features_imputed)

    # Predict rugpull classification & probability
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0][1]

    return {"prediction": int(prediction), "probability": float(probability)}
