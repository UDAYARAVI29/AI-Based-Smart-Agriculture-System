import os
from motor.motor_asyncio import AsyncIOMotorClient
from src.config.settings import settings
from typing import Optional

_client: Optional[AsyncIOMotorClient] = None

def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.MONGO_URI)
    return _client

def get_database():
    client = get_client()
    return client[settings.MONGO_DB]

async def create_indexes():
    db = get_database()
    # Indexes for predictions
    await db.disease_predictions.create_index("created_at")
    await db.irrigation_predictions.create_index("created_at")
    await db.yield_predictions.create_index("created_at")

async def close_client():
    global _client
    if _client:
        _client.close()
        _client = None
