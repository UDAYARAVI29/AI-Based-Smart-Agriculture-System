from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    # Mongo
    MONGO_URI: str = Field(..., env="MONGO_URI")
    MONGO_DB: str = Field("smart_agri", env="MONGO_DB")

    # App
    APP_HOST: str = Field("0.0.0.0", env="APP_HOST")
    APP_PORT: int = Field(8000, env="APP_PORT")

    # Model paths
    DISEASE_MODEL_PATH: str = Field("data/models/disease_model.pth", env="DISEASE_MODEL_PATH")
    IRRIGATION_MODEL_PATH: str = Field("data/models/irrigation_model.pkl", env="IRRIGATION_MODEL_PATH")
    YIELD_MODEL_PATH: str = Field("data/models/yield_model.pkl", env="YIELD_MODEL_PATH")

    # Debug
    DEBUG: bool = Field(True, env="DEBUG")

    class Config:
        env_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        )
        env_file_encoding = "utf-8"

settings = Settings()
