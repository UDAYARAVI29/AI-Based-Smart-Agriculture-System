from fastapi import APIRouter, HTTPException
from src.schemas.irrigation_schema import IrrigationInput
from src.services.irrigation_service import predict_irrigation
from src.services import db_service

router = APIRouter(prefix="/predict/irrigation", tags=["Irrigation Prediction"])


@router.post("/")
async def irrigation_prediction(input_data: IrrigationInput):
    """
    Predict soil moisture & irrigation recommendation.
    Stores prediction in MongoDB.
    """
    try:
        result = predict_irrigation(input_data.dict())

        db_doc = {
            "input_features": input_data.dict(),
            "predicted_moisture": result["predicted_moisture"],
            "recommendation": result["recommendation"]
        }
        inserted_id = await db_service.insert_irrigation_prediction(db_doc)
        result["db_id"] = inserted_id

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
