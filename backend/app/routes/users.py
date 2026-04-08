from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.user import UserCreate, UserResponse, UserLogin, UserUpdate, UserChangePassword
from app.schemas.plant import PlantResponse
from app.services.user_service import create_user, get_user, update_user, login_user, change_password, remove_user
from app.services.plant_service import get_plants_by_user

router = APIRouter(prefix="/users", tags=["Users"])

# user signup
@router.post("/", response_model=UserResponse)
async def signup(user_data: UserCreate):
    try:
        return await create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# user login
@router.post("/login", response_model=UserResponse)
async def login(credentials: UserLogin):
    user = await login_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user

# get user
@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: str):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# update user
@router.put("/{user_id}", response_model=UserResponse)
async def edit_user(user_id: str, update_data: UserUpdate):
    user = await update_user(user_id, update_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# change password
@router.put("/{user_id}/password")
async def update_password(user_id: str, data: UserChangePassword):
    success = await change_password(user_id, data.old_password, data.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid current password or user not found")
    return {"message": "Password updated"}

# delete user
@router.delete("/{user_id}")
async def delete_user(user_id: str):
    success = await remove_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

# get all plants for a user
@router.get("/{user_id}/plants", response_model=List[PlantResponse])
async def get_user_plants(user_id: str):
    return await get_plants_by_user(user_id)