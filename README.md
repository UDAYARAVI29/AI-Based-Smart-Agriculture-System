# AI-Based Smart Agriculture System
## ![Screenshot 2025-11-23 173648](https://github.com/user-attachments/assets/58e699ef-9475-4640-b02c-99c5a7fc5778)
## Overview

The AI-Based Smart Agriculture System is a complete software solution that leverages Artificial Intelligence to provide farming recommendations and predictions. It is a software-only project (no IoT hardware required) and provides:

- Crop disease detection using deep learning (CNN)
- Smart irrigation recommendations using machine learning regression
- Crop yield prediction using regression models
- MongoDB-based prediction history logging
- Modular FastAPI backend architecture

## Project Purpose

Modern agriculture faces challenges such as unpredictable weather, soil degradation, crop diseases and inefficient resource use. This project aims to help farmers and agronomists make data-driven decisions by providing:

- Early detection of plant diseases to prevent spread and reduce losses
- Smart irrigation guidance to conserve water and improve plant health
- Crop yield forecasting to support planning and logistics
- Natural-language recommendations to convert model outputs into actionable advice

## How AI Is Used in This System

### 1. Plant Disease Detection (Deep Learning)

- Model: ResNet-18 (PyTorch)
- Dataset: PlantVillage (or equivalent leaf-image dataset)
- Input: Leaf image uploaded by the user
- Output: Predicted disease class (29+ classes) and confidence score
- Purpose: Detect fungal, bacterial, and other common plant diseases to support early intervention

### 2. Smart Irrigation (Machine Learning)

- Model: RandomForestRegressor (scikit-learn) or similar regression model
- Inputs: temperature, humidity, rainfall, soil type, pH, EC, previous soil moisture (configurable)
- Output: Predicted soil moisture percentage and irrigation recommendation:
  - Irrigation Needed
  - Monitor - Low
  - No Irrigation Required
- Purpose: Prevent over- and under-watering, optimize water usage

### 3. Crop Yield Prediction (Regression)

- Model: Regression model (Random Forest / XGBoost / Linear models)
- Inputs: crop type, season, area, rainfall, temperature, soil characteristics, fertilizer usage
- Output: Predicted yield (tons/hectare)
- Purpose: Help farmers plan harvest, storage and resource allocation

### 4. AI Recommendation Engine (Optional LLM Integration)

- Integration: Google Gemini-Pro (if API key is configured)
- Fallback: Rule-based recommendation generator when LLM is unavailable
- Purpose: Convert model predictions into human-readable, expert-like recommendations:
  - Treatment steps for detected diseases
  - Irrigation scheduling advice
  - Yield improvement suggestions and precautions

## Logging and Trend Analysis

- Every prediction (disease, irrigation, yield) is logged to MongoDB with:
  - Input parameters
  - Prediction result
  - Timestamp
  - Optional user metadata
- Purpose: Build historical data for analytics and visualization

## Tech Stack

### Backend
- Python 3.10+
- FastAPI
- Uvicorn (ASGI server)
- Pydantic for input validation

### Machine Learning / Deep Learning
- PyTorch (for CNN disease model)
- Torchvision (data transforms and models)
- scikit-learn (RandomForestRegressor, preprocessing)
- joblib (model serialization)

### Database
- MongoDB (local or Atlas)
- Motor (async MongoDB driver for FastAPI)

### Data Processing
- pandas, numpy

### Dev / Testing
- pytest (optional)
- VS Code + Thunder Client / Postman for API testing




## Author
**HR Udayaravi**  
AI-Based Smart Agriculture System (2025)

