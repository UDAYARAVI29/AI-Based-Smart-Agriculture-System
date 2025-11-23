from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, Optional

class DiseasePrediction(BaseModel):
    predicted_class: str
    confidence: float
    image_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    meta: Optional[Dict[str, Any]] = None

class IrrigationPrediction(BaseModel):
    input_features: Dict[str, Any]
    predicted_moisture: float
    recommendation: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class YieldPrediction(BaseModel):
    input_features: Dict[str, Any]
    predicted_yield: float
    unit: str = "tons"
    created_at: datetime = Field(default_factory=datetime.utcnow)
