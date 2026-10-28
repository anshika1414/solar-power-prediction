from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["solar_power_db"]

print("Total records:", db.solar_readings.count_documents({}))
print("One record:", db.solar_readings.find_one())

client.close()