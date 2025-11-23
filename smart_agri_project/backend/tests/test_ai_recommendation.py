import sys
import os
sys.path.append(os.path.abspath('src'))
from services.ai_service import generate_recommendation

context = {
    "task_type": "Irrigation Prediction",
    "inputs": {"temperature": 27, "humidity": 70, "soil_moisture": 36.8},
    "prediction": {"predicted_moisture": 36.8, "recommendation": "Monitor - Low"}
}

advice = generate_recommendation(context)
print('---ADVICE START---')
print(advice)
print('---ADVICE END---')
