from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.plant import Location

class PlantModel(BaseModel):
    name: str
    user_id: Optional[str] = None
    parentPlantId: Optional[str] = None
    location: Location
    status: Optional[str] = "🌱 Propagating"
    generation: Optional[int] = 0
    created_at: datetime
    updated_at: datetime