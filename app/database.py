from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URL from environment variable
MONGODB_URL = os.getenv("MONGODB_URL")

# Ensure the URL is loaded correctly
if not MONGODB_URL:
    raise ValueError("MONGODB_URL is not set in the .env file.")

client = AsyncIOMotorClient(MONGODB_URL)  # Use Motor's async client
db = client.get_database("fastapi_crud")

def get_collection(collection_name: str):
    return db[collection_name]

def object_id_to_str(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, ObjectId):
                obj[k] = str(v)
    return obj