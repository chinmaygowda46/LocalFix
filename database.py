import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(MONGO_URL)

db = client[DATABASE_NAME]

# Collections
users_collection = db["users"]
services_collection = db["services"]
providers_collection = db["providers"]
bookings_collection = db["bookings"]
reviews_collection = db["reviews"]


# Test MongoDB connection
try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")
except Exception as e:
    print("MongoDB connection failed!")
    print(e)