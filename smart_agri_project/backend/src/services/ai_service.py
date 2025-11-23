import os
import google.generativeai as genai
from typing import Dict, Any

# Configure API key if available
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

def generate_recommendation(context: Dict[str, Any]) -> str:
    """
    Generate a recommendation based on the context (input data + prediction result).
    Uses Google Generative AI if available, otherwise falls back to rule-based logic.
    """
    
    # Prepare a prompt context
    task_type = context.get("task_type", "General Agriculture")
    inputs = context.get("inputs", {})
    prediction = context.get("prediction", {})
    
    prompt = f"""
    You are an expert agricultural consultant. Analyze the following data and provide a concise, actionable recommendation for the farmer.
    
    Task: {task_type}
    
    Input Conditions:
    {inputs}
    
    Model Prediction:
    {prediction}
    
    Please provide:
    1. A brief analysis of the situation.
    2. Specific steps the farmer should take.
    3. Any precautions.
    
    Keep the tone professional yet encouraging.
    """

    if API_KEY:
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"AI Generation failed: {e}")
            return _fallback_recommendation(task_type, prediction)
    else:
        return _fallback_recommendation(task_type, prediction)

def _fallback_recommendation(task_type: str, prediction: Dict[str, Any]) -> str:
    """
    Simple rule-based fallback if AI is unavailable.
    """
    if task_type == "Disease Detection":
        disease = prediction.get("predicted_class", "Unknown")
        return f"**Detected Disease:** {disease}.\n\n**Recommendation:** Consult a local plant pathologist for specific chemical or organic treatments suitable for {disease}. Isolate the affected plants to prevent spread."
    
    elif task_type == "Irrigation Prediction":
        rec = prediction.get("recommendation", "Monitor")
        return f"**Status:** {rec}.\n\n**Recommendation:** Based on the soil moisture levels, follow the model's advice. Ensure your irrigation system is functioning correctly and check soil moisture manually if in doubt."
        
    elif task_type == "Yield Prediction":
        yield_val = prediction.get("predicted_yield", 0)
        return f"**Forecast:** {yield_val:.2f} tons.\n\n**Recommendation:** To maximize this yield, ensure optimal fertilization and pest control. Monitor weather conditions closely as harvest approaches."
        
    return "Please consult an expert for detailed advice."
