import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from services.ai_service import generate_recommendation
import asyncio

def test_ai():
    context = {
        "task_type": "Irrigation Prediction",
        "inputs": {"temperature": 27, "humidity": 70, "soil_moisture": 36.8},
        "prediction": {"predicted_moisture": 36.8, "recommendation": "Monitor - Low"}
    }

    
    print("Testing AI Recommendation...")
    try:
        advice = generate_recommendation(context)
        print("\nGenerated Advice:")
        print(advice)
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    test_ai()

