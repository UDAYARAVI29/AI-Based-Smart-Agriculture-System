from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.config.database import get_database
import datetime

router = APIRouter()

class SensorRow(BaseModel):
    timestamp: Optional[str] = None
    sensor_id: str
    temp_C: float
    humidity_pct: float
    soil_moisture_pct: float
    pH: float

@router.post("/sensor", summary="Ingest one sensor row")
async def ingest_sensor(row: SensorRow):
    db = get_database()
    collection = db["sensor_readings"]
    doc = row.dict()
    if not doc.get("timestamp"):
        doc["timestamp"] = datetime.datetime.utcnow().isoformat()
    result = await collection.insert_one(doc)
    return {"inserted_id": str(result.inserted_id)}
