from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from src.services.ai_service import generate_recommendation

router = APIRouter(prefix="/ai", tags=["AI Recommendations"])

class AIRequest(BaseModel):
    task_type: str
    inputs: Dict[str, Any]
    prediction: Dict[str, Any]

@router.post("/recommend")
async def get_recommendation(request: AIRequest):
    """
    Get an AI-generated recommendation based on the prediction context.
    """
    try:
        recommendation = generate_recommendation(request.dict())
        return {"recommendation": recommendation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
