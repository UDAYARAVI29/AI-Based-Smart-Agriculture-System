import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from services.irrigation_service import predict_irrigation


def test_prediction():
    input_data = {
        "temperature": 27,
        "humidity": 70,
        "rainfall": 18,
        "soil_type": 2,
        "ph": 4.9,
        "ec": 0.4,
        "previous_moisture": 31.8
    }

    print("Input Data:", input_data)

    # Manually step through the process to debug
    try:
        result = predict_irrigation(input_data)
        print("\nFull Result:", result)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    with open("reproduce_output.txt", "w") as f:
        sys.stdout = f
        sys.stderr = f
        test_prediction()

