import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
import json

BASE = Path(__file__).resolve().parents[2]
RAW = BASE / "data" / "training" / "yield" / "raw"
PROC = BASE / "data" / "processed" / "yield"

PROC.mkdir(parents=True, exist_ok=True)

FILE = list(RAW.glob("*.csv"))[0]

def preprocess():
    df = pd.read_csv(FILE)

    df = df.dropna()
    df["Yield"] = df["Production"] / df["Area"].replace(0, 1)

    df.to_csv(PROC / "cleaned.csv", index=False)

    train, test = train_test_split(df, test_size=0.15, random_state=42)
    train, val = train_test_split(train, test_size=0.176, random_state=42)

    train.to_csv(PROC / "train.csv", index=False)
    val.to_csv(PROC / "val.csv", index=False)
    test.to_csv(PROC / "test.csv", index=False)

    json.dump({
        "rows": len(df),
        "columns": list(df.columns),
        "train": len(train),
        "val": len(val),
        "test": len(test)
    }, open(PROC / "dataset_info.json", "w"), indent=4)

if __name__ == "__main__":
    preprocess()
    print("Yield dataset processed successfully!")
