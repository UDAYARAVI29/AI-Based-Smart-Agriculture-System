# AI-Based Smart Agriculture System

## Overview
The **AI-Based Smart Agriculture System** uses Machine Learning (ML) and Deep Learning (DL) to provide smart recommendations and predictions for farmers. It includes:
- Crop Disease Detection (Deep Learning - CNN)
- Smart Irrigation Recommendation (ML Regression)
- Crop Yield Prediction (ML Regression)
- MongoDB-based prediction history logging
- Fully modular FastAPI backend architecture

## Features
###  Crop Disease Detection
- Upload a leaf image
- Detects 29 crop diseases
- Model: ResNet-18 (PyTorch)

###  Smart Irrigation System
- Predicts soil moisture
- Gives irrigation recommendations:
  - Irrigation Needed
  - Monitor – Low
  - No Irrigation Required
- ML Model: RandomForestRegressor

###  Crop Yield Prediction
- Predicts expected crop yield (tons/hectare)
- Uses rainfall, area, fertilizers, pesticides, season, etc.

###  MongoDB Logging
All predictions are saved automatically for future trend analysis.

---

##   Tech Stack

### Backend
- Python 3.10+
- FastAPI
- PyTorch
- Scikit-Learn
- Motor (Async MongoDB driver)
- Uvicorn
- Pandas / NumPy

### Database
- MongoDB (Atlas or Local)

### ML/DL
- ResNet-18 CNN
- RandomForestRegressor
- Preprocessing Pipelines

---

## API Endpoints

### Disease Detection
`POST /predict/disease`

### Irrigation Prediction
`POST /predict/irrigation`

### Yield Prediction
`POST /predict/yield`

### Health Check
`GET /`

---


##  Getting Started

### 1. Install Dependencies
pip install -r requirements.txt

### 2. Start Backend
uvicorn src.main:app --reload --port 8000

### 3. Open API Docs
Visit:
http://127.0.0.1:8000/docs

---

## 📝 Author
**HR Udayaravi**  
AI-Based Smart Agriculture System (2025)

"""
