"""
Irrigation service
- Loads a trained sklearn regressor from backend/data/models/irrigation_rf.pkl
- Accepts a dict input with expected keys and returns predicted moisture + recommendation.
- Uses a robust Random Forest model trained on:
  ['Humidity', 'Atmospheric_Temp', 'Soil_Temp', 'Dew_Point', 'Previous_Soil_Moisture']
"""

from pathlib import Path
from typing import Dict, Any, Optional
import joblib
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "data" / "models" / "irrigation_rf.pkl"

# Features expected by the NEW model
EXPECTED_FEATURES = [
    "Humidity",
    "Atmospheric_Temp",
    "Soil_Temp",
    "Dew_Point",
    "Previous_Soil_Moisture"
]

_model = None

def _load_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise RuntimeError(f"Irrigation model not found at {MODEL_PATH}. Train model first.")
        _model = joblib.load(MODEL_PATH)
    return _model

def _prepare_dataframe(input_dict: Dict[str, Any]) -> pd.DataFrame:
    """
    Convert input dict into a single-row DataFrame with proper feature mapping.
    """
    # Map frontend aliases to model features
    alias_map = {
        "temperature": "Atmospheric_Temp",
        "humidity": "Humidity",
        "previous_moisture": "Previous_Soil_Moisture",
        "soil_moisture": "Previous_Soil_Moisture", # In case user sends this
        "dew_point": "Dew_Point",
        "soil_temp": "Soil_Temp"
    }
    
    src = dict(input_dict)
    
    # Apply alias mapping
    for k, v in list(src.items()):
        lk = k.lower()
        if lk in alias_map and alias_map[lk] not in src:
            src[alias_map[lk]] = src.pop(k)
            
    # FEATURE ESTIMATION
    # 1. Estimate Dew Point if missing: T - ((100 - RH)/5)
    if "Dew_Point" not in src and "Atmospheric_Temp" in src and "Humidity" in src:
        try:
            T = float(src["Atmospheric_Temp"])
            RH = float(src["Humidity"])
            src["Dew_Point"] = T - ((100 - RH) / 5.0)
        except Exception:
            pass

    # 2. Estimate Soil Temp if missing: T - 2.0 (heuristic)
    if "Soil_Temp" not in src and "Atmospheric_Temp" in src:
        try:
            T = float(src["Atmospheric_Temp"])
            src["Soil_Temp"] = T - 2.0
        except Exception:
            pass
            
    # Build row
    row = {}
    for k in EXPECTED_FEATURES:
        row[k] = src.get(k, 0.0) # Default to 0.0 if missing to prevent crash
        
    return pd.DataFrame([row])

def predict_irrigation(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict soil moisture and give a simple irrigation recommendation.
    """
    model = _load_model()
    
    df = _prepare_dataframe(data)
    
    # Ensure columns are in correct order for the model
    # The model was trained with specific feature order
    X = df[EXPECTED_FEATURES]
    
    # Prediction
    preds = model.predict(X)
    predicted = float(preds[0])

    # Recommendation Logic
    # Thresholds can be adjusted based on crop/soil knowledge
    try:
        if predicted < 25.0:
            rec = "Irrigation Needed"
        elif predicted < 40.0:
            rec = "Monitor - Low"
        else:
            rec = "No Irrigation Required"
    except Exception:
        rec = "No Recommendation"

    return {
        "predicted_moisture": predicted,
        "recommendation": rec
    }
