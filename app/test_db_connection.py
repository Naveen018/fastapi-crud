import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def test_connection():

    MONGODB_URL = os.getenv("MONGODB_URL")

    # Create a new client and connect to the server
    client = MongoClient(MONGODB_URL)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    asyncio.run(test_connection())