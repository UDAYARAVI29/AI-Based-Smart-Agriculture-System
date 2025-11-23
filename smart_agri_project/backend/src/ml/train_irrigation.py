# train_irrigation.py
import pandas as pd
from pathlib import Path
from irrigation_model import train
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    processed = Path("data/processed/irrigation")
    df = pd.read_csv(processed / "cleaned.csv")
    # Example: assume target column is "soil_moisture" or similar. If different, adapt below.
    # Inspect columns:
    print("Columns:", df.columns.tolist())
    # Choose target heuristically
    if "soil_moisture" in df.columns:
        target = "soil_moisture"
    elif "soil_moisture_pct" in df.columns:
        target = "soil_moisture_pct"
    else:
        # fallback: pick first numeric column after timestamp
        num_cols = df.select_dtypes("number").columns.tolist()
        target = num_cols[-1]  # fallback
    print("Using target:", target)

    X = df.drop(columns=[target])
    # drop non-numeric categorical for this basic model (we'll need encoding later)
    X = pd.get_dummies(X, drop_first=True)
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.176, random_state=42)

    train(X_train, y_train, X_val=X_val, y_val=y_val)
