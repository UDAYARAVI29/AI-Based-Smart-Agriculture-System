from fastapi import APIRouter, HTTPException
from src.schemas.yield_schema import YieldInput
from src.services.yield_service import predict_yield
from src.services import db_service

router = APIRouter(prefix="/predict/yield", tags=["Crop Yield Prediction"])


@router.post("/")
async def yield_prediction(input_data: YieldInput):
    """
    Predict crop yield based on inputs.
    Stores output in MongoDB.
    """
    try:
        result = predict_yield(input_data.dict())

        db_doc = {
            "input_features": input_data.dict(),
            "predicted_yield": result["predicted_yield"],
            "unit": result.get("unit", "tons")
        }

        inserted_id = await db_service.insert_yield_prediction(db_doc)
        result["db_id"] = inserted_id

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
