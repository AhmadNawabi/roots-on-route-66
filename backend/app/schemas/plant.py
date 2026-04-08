from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Location(BaseModel):
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")

class PlantCreate(BaseModel):
    name: str
    user_id: Optional[str] = None
    parentPlantId: Optional[str] = None
    location: Location

class ClippingCreate(BaseModel):
    name: str
    user_id: Optional[str] = None
    location: Location

class PlantResponse(BaseModel):
    id: str
    name: str
    user_id: Optional[str] = None
    parentPlantId: Optional[str] = None
    location: Location
    status: Optional[str] = "🌱 Propagating"
    generation: Optional[int] = 0
    created_at: datetime
    updated_at: datetime