from pydantic import BaseModel
from typing import Any, Optional


class YieldInput(BaseModel):
    # Accept flexible types for categorical fields; service will normalize them.
    crop: Optional[Any]
    area: float
    rainfall: float
    temperature: float
    season: Optional[Any]
    soil_type: Optional[Any]
    ph: float
    fertilizer_level: float
