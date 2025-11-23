from pydantic import BaseModel
from typing import Optional


class IrrigationInput(BaseModel):
    # Accept both the original frontend field names and processed dataset names.
    # Fields are optional to allow flexible inputs; service will map aliases.
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    rainfall: Optional[float] = None
    soil_type: Optional[int] = None
    ph: Optional[float] = None
    ec: Optional[float] = None
    previous_moisture: Optional[float] = None

    # Processed dataset-style fields
    Time: Optional[str] = None
    Atmospheric_Temp: Optional[float] = None
    Soil_Temp: Optional[float] = None
    Soil_Moisture: Optional[float] = None
    Dew_Point: Optional[float] = None
