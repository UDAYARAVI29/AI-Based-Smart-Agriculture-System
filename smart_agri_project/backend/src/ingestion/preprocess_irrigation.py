import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
import json

BASE = Path(__file__).resolve().parents[2]
RAW = BASE / "data" / "training" / "irrigation" / "raw"
PROC = BASE / "data" / "processed" / "irrigation"

PROC.mkdir(parents=True, exist_ok=True)

# Detect correct file
csv_files = list(RAW.glob("*.csv"))
xlsx_files = list(RAW.glob("*.xlsx"))

if csv_files:
    FILE = csv_files[0]
elif xlsx_files:
    FILE = xlsx_files[0]
else:
    raise FileNotFoundError("No CSV or Excel irrigation data found in raw folder.")


def preprocess():
    # Load the file
    if FILE.suffix == ".xlsx":
        df = pd.read_excel(FILE)
    else:
        df = pd.read_csv(FILE)

    # Remove missing values
    df = df.dropna()

    # Normalize numeric columns
    num_cols = df.select_dtypes("number").columns
    df[num_cols] = (df[num_cols] - df[num_cols].mean()) / df[num_cols].std()

    # Save cleaned data
    df.to_csv(PROC / "cleaned.csv", index=False)

    # Train/Val/Test Split
    train, test = train_test_split(df, test_size=0.15, random_state=42)
    train, val = train_test_split(train, test_size=0.176, random_state=42)

    train.to_csv(PROC / "train.csv", index=False)
    val.to_csv(PROC / "val.csv", index=False)
    test.to_csv(PROC / "test.csv", index=False)

    # Metadata
    json.dump({
        "rows": len(df),
        "columns": list(df.columns),
        "train": len(train),
        "val": len(val),
        "test": len(test)
    }, open(PROC / "dataset_info.json", "w"), indent=4)


if __name__ == "__main__":
    preprocess()
    print("Irrigation dataset processed successfully!")
