from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from logs.logger import get_logger

logger = get_logger("RealtimeSensorDataAPI")

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/sensor_data")
client = AsyncIOMotorClient(MONGO_URI)
db = client["sensor_data"]

def initialize_db():
    logger.info(f"Connected to MongoDB at {MONGO_URI}")