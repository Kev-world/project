from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')
MONGODB_NAME = os.getenv('MONGODB_NAME')

client = AsyncIOMotorClient(MONGODB_URL)
db = client.get_database(MONGODB_NAME)