from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    username: str
    zip_code: str
    email: EmailStr
    password: str
    bio: Optional[str] = None
    profile_picture: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    zip_code: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str

class UserResponse(BaseModel):
    id: str
    name: str
    username: str
    zip_code: str
    email: EmailStr
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    plants: List[str] = []
    created_at: datetime
    updated_at: datetime