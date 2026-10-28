import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGO_URI")

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    print("MongoDB connected successfully!")
except Exception as e:
    print("Connection failed:", e)
