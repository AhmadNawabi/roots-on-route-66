from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = AsyncIOMotorClient(MONGODB_URI)

db = client["route66"]

users_collection = db["users"]
plants_collection = db["plants"]


async def create_indexes():
    """requires email to be unique"""
    await users_collection.create_index("email", unique=True)
