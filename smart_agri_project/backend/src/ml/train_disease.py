# train_disease.py
# Run this to train the disease classifier
import argparse
from pathlib import Path
from disease_model import train_model

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--processed_dir", type=str, default="data/processed/disease", help="path to processed disease folder")
    parser.add_argument("--epochs", type=int, default=6)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-4)
    args = parser.parse_args()

    processed_dir = Path(args.processed_dir)
    print("Training with processed dir:", processed_dir)
    train_model(processed_dir, epochs=args.epochs, batch_size=args.batch_size, lr=args.lr)
