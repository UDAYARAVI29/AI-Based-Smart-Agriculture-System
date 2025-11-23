# train_yield.py
import pandas as pd
from pathlib import Path
from yield_model import train
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    processed = Path("data/processed/yield")
    df = pd.read_csv(processed / "cleaned.csv")
    print("Columns:", df.columns.tolist())

    # Ensure 'Production' and 'Area' exist; create 'Yield' if missing
    if "Yield" not in df.columns:
        if "Production" in df.columns and "Area" in df.columns:
            df["Yield"] = df["Production"] / df["Area"].replace(0, 1)
        else:
            raise RuntimeError("No Yield/Production/Area columns found in processed yield CSV.")

    # Select features - encode categorical columns
    y = df["Yield"]
    X = df.drop(columns=["Yield", "Production"])  # drop Production to predict Yield
    X = pd.get_dummies(X, drop_first=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.176, random_state=42)

    train(X_train, y_train, X_val=X_val, y_val=y_val)
