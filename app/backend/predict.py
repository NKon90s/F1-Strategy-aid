import joblib
import pandas as pd
from pathlib import Path


# Identifying the root library parent[2] provides the F1_strategy_aid lib
BASE_DIR = Path(__file__).resolve().parents[2]
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




if __name__ == "__main__":

    data = {
        "location": "Sakhir",
        "avg_track_temperature": 28.81,
        "track_length": 5412,
        "n_of_corners": 15,
        "degradation": "Very High",
        "overtake_difficulty": "Hard",
        "avg_pit_time": 25.84,
        "driver_number": 1,
        "full_name": "Max VERSTAPPEN",
        "team_name": "Red Bull Racing",
        "grid_category": "Top-Field",
        "dist_hard": 0.06,
        "dist_medium": 0.11,
        "dist_soft": 0.83,
        "driver_baseline_pace": 98.93,
        "grid_position": 1
    }

    prediction = predict_compound(data)
    print(prediction)