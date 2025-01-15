import os
import motor.motor_asyncio

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["baymax"]

recipes_collection = db["recipes"]
nutritional_info_collection = db["nutritionalinfo"]
