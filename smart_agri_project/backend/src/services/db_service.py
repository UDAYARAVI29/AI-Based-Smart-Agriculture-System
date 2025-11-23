from src.config.database import get_database
import datetime
from bson import ObjectId
from typing import Dict, Any, List, Optional

db = get_database()

def _serialize_id(doc: Dict[str, Any]) -> Dict[str, Any]:
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


async def insert_disease_prediction(doc: Dict[str, Any]) -> str:
    doc["created_at"] = datetime.datetime.utcnow().isoformat()
    result = await db.disease_predictions.insert_one(doc)
    return str(result.inserted_id)

async def get_disease_prediction(pred_id: str) -> Optional[Dict[str, Any]]:
    doc = await db.disease_predictions.find_one({"_id": ObjectId(pred_id)})
    return _serialize_id(doc)


async def insert_irrigation_prediction(doc: Dict[str, Any]) -> str:
    doc["created_at"] = datetime.datetime.utcnow().isoformat()
    result = await db.irrigation_predictions.insert_one(doc)
    return str(result.inserted_id)


async def insert_yield_prediction(doc: Dict[str, Any]) -> str:
    doc["created_at"] = datetime.datetime.utcnow().isoformat()
    result = await db.yield_predictions.insert_one(doc)
    return str(result.inserted_id)


async def get_recent_predictions(collection: str, limit: int = 20) -> List[Dict[str, Any]]:
    docs = await db[collection].find().sort("created_at", -1).to_list(length=limit)
    return [_serialize_id(d) for d in docs]
