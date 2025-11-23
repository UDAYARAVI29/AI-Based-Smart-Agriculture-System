# yield_model.py
# sklearn RandomForest for crop yield prediction

import joblib
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt

MODEL_DIR = Path(__file__).resolve().parents[2] / "data" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "yield_rf.pkl"


def train(X_train, y_train, X_val=None, y_val=None, n_estimators=300):
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # save model
    joblib.dump(model, MODEL_PATH)
    print("Saved yield prediction model:", MODEL_PATH)

    # validation (if provided)
    if X_val is not None:
        preds = model.predict(X_val)

        # FIXED: RMSE without using squared=False
        rmse = sqrt(mean_squared_error(y_val, preds))
        r2 = r2_score(y_val, preds)

        print("Yield val RMSE:", rmse)
        print("Yield val R2:", r2)

    return MODEL_PATH


def load():
    return joblib.load(MODEL_PATH)


def predict(X):
    model = load()
    return model.predict(X)
