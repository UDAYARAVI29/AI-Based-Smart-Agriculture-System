import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "training" / "irrigation" / "raw"
MODEL_DIR = BASE_DIR / "data" / "models"
TRAIN_CSV = DATA_DIR / "soil_data_incl_rain_v3.csv"
MODEL_PATH = MODEL_DIR / "irrigation_rf.pkl"


def train_model():
    print(f"Loading data from {TRAIN_CSV}...")
    df = pd.read_csv(TRAIN_CSV)
    
    # Sort by time to ensure lag is correct
    if 'Time' in df.columns:
        df['Time'] = pd.to_datetime(df['Time'])
        df = df.sort_values('Time')
    
    # Normalize Soil_Moisture to 0-100 range if it looks like 0-255 data
    # Max value observed was ~238, so likely 8-bit sensor data.
    if df['Soil_Moisture'].max() > 100:
        print("Normalizing Soil_Moisture from 0-255 to 0-100 range...")
        df['Soil_Moisture'] = (df['Soil_Moisture'] / 255.0) * 100.0
    
    # Create Lagged Feature: Previous_Soil_Moisture
    # We assume the data is a continuous time series
    df['Previous_Soil_Moisture'] = df['Soil_Moisture'].shift(1)

    
    # Drop the first row which will have NaN for Previous_Soil_Moisture
    df = df.dropna()
    
    # Define Features and Target
    # We exclude 'Time' as it's not a good feature for generalization
    # We exclude 'Soil_Moisture' from features because it's the target
    target = 'Soil_Moisture'
    
    # Features available in the dataset
    # Based on inspection: Humidity, Atmospheric_Temp, Soil_Temp, Dew_Point
    # And our new feature: Previous_Soil_Moisture
    features = ['Humidity', 'Atmospheric_Temp', 'Soil_Temp', 'Dew_Point', 'Previous_Soil_Moisture']
    
    # Check if all features exist
    missing_features = [f for f in features if f not in df.columns]
    if missing_features:
        raise ValueError(f"Missing features in dataset: {missing_features}")
        
    print(f"Training with features: {features}")
    
    X = df[features]
    y = df[target]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest
    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    
    print(f"Model Evaluation:")
    print(f"MSE: {mse:.4f}")
    print(f"R2 Score: {r2:.4f}")
    
    # Save Model
    print(f"Saving model to {MODEL_PATH}...")
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("Done.")

if __name__ == "__main__":
    train_model()
