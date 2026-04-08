from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.schemas.plant import PlantCreate, PlantResponse, ClippingCreate
from app.services.plant_service import (
    create_plant,
    get_plant,
    update_plant,
    remove_plant,
    claim_plant,
    create_clipping,
    get_lineage,
    get_plants_by_user
)

router = APIRouter(prefix="/plants", tags=["Plants"])

# create plant — anonymous or by user
@router.post("/", response_model=PlantResponse)
async def add_plant(plant_data: PlantCreate):
    return await create_plant(plant_data, plant_data.user_id)

# get plant
@router.get("/{plant_id}", response_model=PlantResponse)
async def read_plant(plant_id: str):
    plant = await get_plant(plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

# update plant
@router.put("/{plant_id}", response_model=PlantResponse)
async def edit_plant(plant_id: str, update_data: dict):
    plant = await update_plant(plant_id, update_data)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

# delete plant
@router.delete("/{plant_id}")
async def delete_plant(plant_id: str):
    success = await remove_plant(plant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plant not found")
    return {"message": "Plant deleted"}

# claim an anonymous plant
@router.post("/{plant_id}/claim", response_model=PlantResponse)
async def claim_existing_plant(plant_id: str, user_id: str):
    plant = await claim_plant(plant_id, user_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

# take a clipping from a plant
@router.post("/{plant_id}/clipping", response_model=PlantResponse)
async def take_clipping(plant_id: str, clipping_data: ClippingCreate):
    clipping = await create_clipping(plant_id, clipping_data)
    if not clipping:
        raise HTTPException(status_code=404, detail="Parent plant not found")
    return clipping

# get full lineage of a plant
@router.get("/{plant_id}/lineage", response_model=List[PlantResponse])
async def plant_lineage(plant_id: str):
    return await get_lineage(plant_id)
