from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import json

class SensorDataBase(BaseModel):
    device_id: str = Field(..., description="Unique identifier for the device")
    temperature: float = Field(..., ge=-273.15, description="Temperature in Celsius")
    pressure: float = Field(..., ge=0, description="Pressure in hPa")
    timestamp: datetime

    @validator('temperature')
    def validate_temperature(cls, v):
        if v < -273.15:  # Absolute zero in Celsius
            raise ValueError("Temperature cannot be below absolute zero")
        return v

    class Config:
        schema_extra = {
            "example": {
                "device_id": "sensor_001",
                "temperature": 25.0,
                "pressure": 1013.25,
                "timestamp": "2024-03-14T12:00:00Z"
            }
        }

class SensorDataResponse(SensorDataBase):
    temperature_f: float
    pressure_psi: float 