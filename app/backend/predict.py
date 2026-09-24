import joblib
import pandas as pd

compound_model = joblib.load("models\\final_xgb_tyre_prediction_model.joblib")
stint_model = joblib.load("models\\final_xgb_first_stint_prediction_model.joblib")

def predict_compound(data: dict):
    X = pd.DataFrame([data])
    prediction = compound_model.predict(X)

    return prediction
 

def predict_stint(data: dict):
    X = pd.DataFrame([data])
    prediction = stint_model.predict(X)
    
    return prediction