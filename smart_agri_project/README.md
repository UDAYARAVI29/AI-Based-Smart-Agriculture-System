AI-Based Smart Agriculture System
A Machine Learning + Deep Learning powered platform for smart farming automation
Overview

The AI-Based Smart Agriculture System is an end-to-end software solution that uses Machine Learning (ML) and Deep Learning (DL) to assist farmers and agronomists in making data-driven decisions—without needing any IoT sensors or hardware.

This project provides:

✔ Plant Disease Detection (CNN + PyTorch)
✔ Smart Irrigation Prediction (Random Forest Model)
✔ Crop Yield Forecasting (Regression Model)
✔ FastAPI Backend
✔ MongoDB for storing predictions
✔ Fully production-ready folder structure

This system helps optimize crop health, water usage, and agricultural productivity using advanced AI models.

Features
1. Plant Disease Detection

Upload a plant leaf image

Deep Learning model (ResNet-18) detects 29 disease classes

Uses PlantVillage dataset

Outputs:

Predicted Disease

Confidence Score

Saves result to MongoDB

2. Smart Irrigation Recommendation

Predicts soil moisture based on environmental values

Provides actionable irrigation advice:

Irrigation Needed

Monitor - Low

No Irrigation Required

Helps prevent water wastage and crop water stress

3. Crop Yield Prediction

Predicts yield using:

Crop type

Season

Rainfall

Fertilizer usage

Pesticides

Cultivation area

Helps in planning and farming optimization

4. FastAPI Backend

Handles AI inference

Clean router structure

Async MongoDB integration

CORS-enabled for frontend

5. MongoDB Storage

Stores:

Disease predictions

Irrigation results

Yield forecasts

Useful for analytics dashboards and historical insights.

Tech Stack
Backend

Python 3.10+

FastAPI

Uvicorn

PyTorch

Scikit-Learn

Torchvision

Pydantic

Motor (Async MongoDB driver)

Database

MongoDB / MongoDB Atlas

Model Training

Jupyter Notebook

Pandas, NumPy

Real agricultural datasets

Tools

VS Code

Thunder Client/Postman

Git & GitHub

API Endpoints
Disease Prediction
POST /predict/disease

Irrigation Prediction
POST /predict/irrigation

Yield Prediction
POST /predict/yield


▶How to Run the Backend
1️Create virtual environment
python -m venv venv

2️Activate it (Windows)
venv\Scripts\activate

3️Install dependencies
pip install -r requirements.txt

4️Set MongoDB connection

Edit .env:

MONGO_URL=mongodb://localhost:27017
DB_NAME=smart_agri

5️Start the server
uvicorn src.main:app --reload --port 8000

6️Open in browser
http://127.0.0.1:8000

Testing the API

Use Thunder Client / Postman / VS Code:

Test Disease:

Upload leaf image to:

POST /predict/disease

Test Irrigation:

Send JSON body to:

POST /predict/irrigation

Test Yield:

Send JSON body to:

POST /predict/yield

Datasets Used
Plant Disease Dataset

PlantVillage (39k images)

29 disease classes

Soil & Irrigation Dataset

Contains humidity, temp, soil moisture

Cleaned and processed

Crop Production Dataset

Indian crop yield data

Cleaned & encoded for ML

Project Benefits

Reduces crop losses

Saves water

Improves farmer decision-making

No hardware required

Easy-to-use API

Scalable AI architecture

Author

HR Udayaravi
AI & Software Developer