from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserModel(BaseModel):
    name: str
    username: str
    zip_code: str
    email: EmailStr
    password: str
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    plants: List[str] = []
    created_at: datetime
    updated_at: datetime