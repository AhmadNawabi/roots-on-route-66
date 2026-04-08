from app.config.mongodb import db, users_collection
from app.schemas.plant import PlantCreate, PlantResponse, ClippingCreate
from app.models.plant import PlantModel
from bson import ObjectId
from bson.errors import InvalidId
from typing import List, Optional
from datetime import datetime

async def create_plant(data: PlantCreate, user_id: Optional[str] = None) -> PlantResponse:
    now = datetime.utcnow()

    plant_model = PlantModel(
        name=data.name,
        user_id=user_id,
        parentPlantId=data.parentPlantId,
        location=data.location,
        created_at=now,
        updated_at=now
    )

    result = await db.plants.insert_one(plant_model.dict())
    plant_id = str(result.inserted_id)

    # only link to user if user_id is provided
    if user_id:
        try:
            await users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$push": {"plants": plant_id}}
            )
        except InvalidId:
            pass

    return PlantResponse(id=plant_id, **plant_model.dict())

async def get_plant(plant_id: str) -> Optional[PlantResponse]:
    try:
        oid = ObjectId(plant_id)
    except InvalidId:
        return None

    plant = await db.plants.find_one({"_id": oid})
    if not plant:
        return None

    plant_model = PlantModel(**{k: v for k, v in plant.items() if k != "_id"})
    return PlantResponse(id=str(plant["_id"]), **plant_model.dict())

async def update_plant(plant_id: str, update_data: dict) -> Optional[PlantResponse]:
    try:
        oid = ObjectId(plant_id)
    except InvalidId:
        return None

    existing = await db.plants.find_one({"_id": oid})
    if not existing:
        return None

    updated_model = PlantModel(**{
        **{k: v for k, v in existing.items() if k != "_id"},
        **update_data,
        "updated_at": datetime.utcnow()
    })

    await db.plants.update_one(
        {"_id": oid},
        {"$set": updated_model.dict()}
    )
    return await get_plant(plant_id)

async def remove_plant(plant_id: str) -> bool:
    try:
        oid = ObjectId(plant_id)
    except InvalidId:
        return False

    # remove plant id from user's plants array if it has a user
    plant = await db.plants.find_one({"_id": oid})
    if not plant:
        return False

    if plant.get("user_id"):
        try:
            await users_collection.update_one(
                {"_id": ObjectId(plant["user_id"])},
                {"$pull": {"plants": plant_id}}
            )
        except InvalidId:
            pass

    result = await db.plants.delete_one({"_id": oid})
    return result.deleted_count == 1

async def claim_plant(plant_id: str, user_id: str) -> Optional[PlantResponse]:
    try:
        oid = ObjectId(plant_id)
        ObjectId(user_id)
    except InvalidId:
        return None

    plant = await db.plants.find_one({"_id": oid})
    if not plant:
        return None

    # update plant with user_id
    await db.plants.update_one(
        {"_id": oid},
        {"$set": {"user_id": user_id, "updated_at": datetime.utcnow()}}
    )

    # add plant to user's plants array
    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"plants": plant_id}}
    )

    return await get_plant(plant_id)

async def create_clipping(parent_plant_id: str, data: ClippingCreate) -> Optional[PlantResponse]:
    # make sure parent exists
    parent = await get_plant(parent_plant_id)
    if not parent:
        return None

    now = datetime.utcnow()

    plant_model = PlantModel(
        name=data.name,
        user_id=data.user_id,
        parentPlantId=parent_plant_id,
        location=data.location,
        created_at=now,
        updated_at=now
    )

    result = await db.plants.insert_one(plant_model.dict())
    plant_id = str(result.inserted_id)

    # only link to user if user_id provided
    if data.user_id:
        try:
            await users_collection.update_one(
                {"_id": ObjectId(data.user_id)},
                {"$push": {"plants": plant_id}}
            )
        except InvalidId:
            pass

    return PlantResponse(id=plant_id, **plant_model.dict())

async def get_lineage(plant_id: str) -> List[PlantResponse]:
    lineage = []
    visited = set()

    current = await get_plant(plant_id)
    if current:
        lineage.append(current)
        visited.add(plant_id)

    while current and current.parentPlantId:
        if current.parentPlantId in visited:
            break
        visited.add(current.parentPlantId)
        parent = await get_plant(current.parentPlantId)
        if not parent:
            break
        lineage.append(parent)
        current = parent

    return lineage

async def get_plants_by_user(user_id: str) -> List[PlantResponse]:
    try:
        ObjectId(user_id)
    except InvalidId:
        return []

    plants = await db.plants.find({"user_id": user_id}).to_list(length=None)
    result = []
    for plant in plants:
        plant_model = PlantModel(**{k: v for k, v in plant.items() if k != "_id"})
        result.append(PlantResponse(id=str(plant["_id"]), **plant_model.dict()))
    return result
from app.config.mongodb import db, users_collection
from app.schemas.plant import PlantCreate, PlantResponse, ClippingCreate
from app.models.plant import PlantModel
from bson import ObjectId
from bson.errors import InvalidId
from typing import List, Optional
from datetime import datetime

async def create_plant(data: PlantCreate, user_id: Optional[str] = None) -> PlantResponse:
    now = datetime.utcnow()

    plant_model = PlantModel(
        name=data.name,
        user_id=user_id,
        parentPlantId=data.parentPlantId,
        location=data.location,
        status="🌱 Propagating",
        generation=0,
        created_at=now,
        updated_at=now
    )

    result = await db.plants.insert_one(plant_model.dict())
    plant_id = str(result.inserted_id)

    if user_id:
        try:
            await users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$push": {"plants": plant_id}}
            )
        except InvalidId:
            pass

    return PlantResponse(id=plant_id, **plant_model.dict())

async def get_plant(plant_id: str) -> Optional[PlantResponse]:
    try:
        oid = ObjectId(plant_id)
    except InvalidId:
        return None

    plant = await db.plants.find_one({"_id": oid})
    if not plant:
        return None

    plant_model = PlantModel(**{k: v for k, v in plant.items() if k != "_id"})
    return PlantResponse(id=str(plant["_id"]), **plant_model.dict())

async def update_plant(plant_id: str, update_data: dict) -> Optional[PlantResponse]:
    try:
        oid = ObjectId(plant_id)
    except InvalidId:
        return None

    existing = await db.plants.find_one({"_id": oid})
    if not existing:
        return None

    updated_model = PlantModel(**{
        **{k: v for k, v in existing.items() if k != "_id"},
        **update_data,
        "updated_at": datetime.utcnow()
    })

    await db.plants.update_one(
        {"_id": oid},
        {"$set": updated_model.dict()}
    )
    return await get_plant(plant_id)

async def remove_plant(plant_id: str) -> bool:
    try:
        oid = ObjectId(plant_id)
    except InvalidId:
        return False

    plant = await db.plants.find_one({"_id": oid})
    if not plant:
        return False

    if plant.get("user_id"):
        try:
            await users_collection.update_one(
                {"_id": ObjectId(plant["user_id"])},
                {"$pull": {"plants": plant_id}}
            )
        except InvalidId:
            pass

    result = await db.plants.delete_one({"_id": oid})
    return result.deleted_count == 1

async def claim_plant(plant_id: str, user_id: str) -> Optional[PlantResponse]:
    try:
        oid = ObjectId(plant_id)
        ObjectId(user_id)
    except InvalidId:
        return None

    plant = await db.plants.find_one({"_id": oid})
    if not plant:
        return None

    await db.plants.update_one(
        {"_id": oid},
        {"$set": {"user_id": user_id, "updated_at": datetime.utcnow()}}
    )

    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"plants": plant_id}}
    )

    return await get_plant(plant_id)

async def create_clipping(parent_plant_id: str, data: ClippingCreate) -> Optional[PlantResponse]:
    parent = await get_plant(parent_plant_id)
    if not parent:
        return None

    now = datetime.utcnow()

    # generation automatically increases from parent
    plant_model = PlantModel(
        name=data.name,
        user_id=data.user_id,
        parentPlantId=parent_plant_id,
        location=data.location,
        status="🌱 Propagating",
        generation=(parent.generation or 0) + 1,
        created_at=now,
        updated_at=now
    )

    result = await db.plants.insert_one(plant_model.dict())
    plant_id = str(result.inserted_id)

    if data.user_id:
        try:
            await users_collection.update_one(
                {"_id": ObjectId(data.user_id)},
                {"$push": {"plants": plant_id}}
            )
        except InvalidId:
            pass

    return PlantResponse(id=plant_id, **plant_model.dict())

async def get_lineage(plant_id: str) -> List[PlantResponse]:
    lineage = []
    visited = set()

    current = await get_plant(plant_id)
    if current:
        lineage.append(current)
        visited.add(plant_id)

    while current and current.parentPlantId:
        if current.parentPlantId in visited:
            break
        visited.add(current.parentPlantId)
        parent = await get_plant(current.parentPlantId)
        if not parent:
            break
        lineage.append(parent)
        current = parent

    return lineage

async def get_plants_by_user(user_id: str) -> List[PlantResponse]:
    try:
        ObjectId(user_id)
    except InvalidId:
        return []

    plants = await db.plants.find({"user_id": user_id}).to_list(length=None)
    result = []
    for plant in plants:
        plant_model = PlantModel(**{k: v for k, v in plant.items() if k != "_id"})
        result.append(PlantResponse(id=str(plant["_id"]), **plant_model.dict()))
    return result
