from app.config.mongodb import users_collection
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.models.user import UserModel
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

async def create_user(user_data: UserCreate) -> UserResponse:
    now = datetime.utcnow()

    user_model = UserModel(
        name=user_data.name,
        username=user_data.username,
        zip_code=user_data.zip_code,
        email=user_data.email,
        password=hash_password(user_data.password),
        bio=user_data.bio,
        profile_picture=user_data.profile_picture,
        plants=[],
        created_at=now,
        updated_at=now
    )

    try:
        result = await users_collection.insert_one(user_model.dict())
        return UserResponse(id=str(result.inserted_id), **user_model.dict())
    except DuplicateKeyError:
        raise ValueError("Email already exists")

async def login_user(email: str, password: str) -> UserResponse | None:
    user = await users_collection.find_one({"email": email})
    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None
    user["id"] = str(user["_id"])
    user.setdefault("plants", [])
    return UserResponse(**user)

async def get_user(user_id: str) -> UserResponse | None:
    try:
        oid = ObjectId(user_id)
    except InvalidId:
        return None

    user = await users_collection.find_one({"_id": oid})
    if not user:
        return None

    user_model = UserModel(**{k: v for k, v in user.items() if k != "_id"})
    return UserResponse(id=str(user["_id"]), **user_model.dict())

async def update_user(user_id: str, update_data: UserUpdate) -> UserResponse | None:
    try:
        oid = ObjectId(user_id)
    except InvalidId:
        return None

    existing = await users_collection.find_one({"_id": oid})
    if not existing:
        return None

    changes = {k: v for k, v in update_data.dict().items() if v is not None}

    updated_model = UserModel(**{
        **{k: v for k, v in existing.items() if k != "_id"},
        **changes,
        "updated_at": datetime.utcnow()
    })

    await users_collection.update_one(
        {"_id": oid},
        {"$set": updated_model.dict()}
    )
    return await get_user(user_id)

async def change_password(user_id: str, old_password: str, new_password: str) -> bool:
    try:
        oid = ObjectId(user_id)
    except InvalidId:
        return False

    user = await users_collection.find_one({"_id": oid})
    if not user:
        return False

    if not verify_password(old_password, user["password"]):
        return False

    await users_collection.update_one(
        {"_id": oid},
        {"$set": {
            "password": hash_password(new_password),
            "updated_at": datetime.utcnow()
        }}
    )
    return True

async def remove_user(user_id: str) -> bool:
    try:
        oid = ObjectId(user_id)
    except InvalidId:
        return False

    result = await users_collection.delete_one({"_id": oid})
    return result.deleted_count == 1