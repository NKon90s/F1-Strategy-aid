import joblib
import pandas as pd
from pathlib import Path
import numpy as np


# Identifying the root library parent[1] provides the backend lib
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"  # locate the models folder

compound_model_path = MODEL_DIR / "final_xgb_tyre_prediction_model.joblib"
stint_model_path = MODEL_DIR / "final_xgb_first_stint_prediction_model.joblib"

compound_model = joblib.load(compound_model_path)
stint_model = joblib.load(stint_model_path)


def predict_compound(data: dict):
    X = pd.DataFrame([data])
     
    # Encoded prediction: 0, 1, or 2
    pred_encoded = compound_model.predict(X)[0]
    # Probabilities in model class order
    probabilities = compound_model.predict_proba(X)[0]

    # LabelEncoder mapping
    class_names = {
        0: "HARD",
        1: "MEDIUM",
        2: "SOFT"
    }

    prediction = class_names[int(pred_encoded)]

    return {
        "prediction": prediction,
        "probabilities": {
            "HARD": float(probabilities[0]),
            "MEDIUM": float(probabilities[1]),
            "SOFT": float(probabilities[2])
        }
    }


def predict_stint(data: dict):
    X = pd.DataFrame([data])
    pred = stint_model.predict(X)[0]
    
    return pred



