from pydantic import BaseModel

class DiseasePredictionResponse(BaseModel):
    predicted_class: str
    confidence: float
