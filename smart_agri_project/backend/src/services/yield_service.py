"""
Yield service
- Loads a trained sklearn regressor from backend/data/models/yield_rf.pkl
- Optionally loads a scaler from backend/data/models/yield_scaler.pkl
- Handles simple categorical encoding (via provided maps or one-hot fallback)
- Returns predicted yield and unit

This service is robust to minor variations in input (strings or integers for categorical features).
"""

from pathlib import Path
from typing import Dict, Any, Optional
import joblib
import pandas as pd
import numpy as np
import os

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "data" / "models" / "yield_rf.pkl"
SCALER_PATH = BASE_DIR / "data" / "models" / "yield_scaler.pkl"
# your uploaded crop dataset for reference
DEFAULT_RAW_CSV_PATH = Path("/mnt/data/e1cb9f46-e091-4a44-8f35-4cd14be6e3ab.csv")

# Default expected features (adapt these to your processed CSV)
EXPECTED_FEATURES = [
    "crop",          # encoded (int) or string (will be encoded)
    "area",          # numeric (hectares)
    "rainfall",      # numeric (mm)
    "temperature",   # numeric (C)
    "season",        # encoded int or string (eg "Kharif")
    "soil_type",     # int or string
    "ph",
    "fertilizer_level"
]


DEFAULT_CROP_MAP = {
    # These are example mappings; 
    "rice": 0,
    "wheat": 1,
    "maize": 2,
    "cotton": 3,
    "sugarcane": 4
}

DEFAULT_SEASON_MAP = {
    "kharif": 0,
    "rabi": 1,
    "summer": 2,
    "winter": 3,
    "whole_year": 4
}

# load model and scaler lazily
_model = None
_scaler = None

def _load_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise RuntimeError(f"Yield model not found at {MODEL_PATH}. Train the model first.")
        _model = joblib.load(MODEL_PATH)
    return _model

def _load_scaler():
    global _scaler
    if _scaler is None:
        if SCALER_PATH.exists():
            _scaler = joblib.load(SCALER_PATH)
        else:
            _scaler = None
    return _scaler

def _prepare_input(data: Dict[str, Any],
                   crop_map: Optional[Dict[str,int]] = None,
                   season_map: Optional[Dict[str,int]] = None) -> pd.DataFrame:
    """
    Prepare a DataFrame row for prediction:
    - Map categorical fields using provided maps (case-insensitive)
    - Convert numeric strings to numbers
    - One-hot encode remaining string categories as fallback
    """
    crop_map = crop_map or DEFAULT_CROP_MAP
    season_map = season_map or DEFAULT_SEASON_MAP

    
    row = {k: data.get(k, np.nan) for k in EXPECTED_FEATURES}
    for k, v in data.items():
        if k not in row:
            row[k] = v

    # Normalize keys
    df = pd.DataFrame([row])

    # Map crop (if string)
    if "crop" in df.columns:
        val = df.at[0, "crop"]
        if isinstance(val, str):
            key = val.strip().lower()
            df.at[0, "crop"] = crop_map.get(key, np.nan)

    # Map season
    if "season" in df.columns:
        val = df.at[0, "season"]
        if isinstance(val, str):
            key = val.strip().lower()
            df.at[0, "season"] = season_map.get(key, np.nan)

    # Convert numeric columns where possible
    for col in df.columns:
        if col in ["crop", "season", "soil_type"]:
            # keep as-is (may be categorical)
            continue
        try:
            df[col] = pd.to_numeric(df[col], errors="ignore")
        except Exception:
            pass

    return df

def _align_features(df: pd.DataFrame, scaler, model_feature_names=None) -> pd.DataFrame:
    """
    Align features for model input (one-hot encode text categories and scale if scaler provided).
    If scaler has feature_names_in_, use that ordering.
    """
    df_enc = pd.get_dummies(df, drop_first=True)

    expected_cols = None
    if scaler is not None and hasattr(scaler, "feature_names_in_"):
        expected_cols = list(scaler.feature_names_in_)
    if expected_cols is None and model_feature_names is not None:
        expected_cols = list(model_feature_names)

    if expected_cols is not None:
        for c in expected_cols:
            if c not in df_enc.columns:
                df_enc[c] = 0.0
        df_enc = df_enc[expected_cols]
        if scaler is not None:
            try:
                X = scaler.transform(df_enc)
                X = pd.DataFrame(X, columns=expected_cols)
                return X
            except Exception:
                return df_enc
        return df_enc

    # fallback: use numeric columns
    numeric_cols = df_enc.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) == 0:
        # if nothing numeric, fallback to all columns
        return df_enc
    if scaler is not None:
        try:
            X = scaler.transform(df_enc[numeric_cols])
            X = pd.DataFrame(X, columns=numeric_cols)
            return X
        except Exception:
            return df_enc[numeric_cols]
    return df_enc[numeric_cols]

def predict_yield(data: Dict[str, Any],
                  crop_map: Optional[Dict[str,int]] = None,
                  season_map: Optional[Dict[str,int]] = None) -> Dict[str, Any]:
    """
    Predict yield based on input dictionary.
    Returns { "predicted_yield": float, "unit": "tons" }
    """
    model = _load_model()
    scaler = _load_scaler()

    df = _prepare_input(data, crop_map=crop_map, season_map=season_map)
    model_feature_names = getattr(model, "feature_names_in_", None)
    X = _align_features(df, scaler, model_feature_names)

    if X.shape[1] == 0:
        raise RuntimeError("No valid input features available for prediction. Check input payload.")

    preds = model.predict(X)
    predicted = float(preds[0])

    return {
        "predicted_yield": predicted,
        "unit": "tons"
    }

# Optional helper: load uploaded raw crop dataset for inspections
def inspect_uploaded_raw(path: Optional[Path] = None) -> pd.DataFrame:
    p = Path(path) if path else DEFAULT_RAW_CSV_PATH
    if not p.exists():
        raise FileNotFoundError(f"Raw CSV not found at {p}")
    return pd.read_csv(p)
