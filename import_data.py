import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["solar_power_db"]
collection = db["solar_readings"]

data = pd.read_csv("merged_solar_data.csv")
records = data.to_dict("records")

collection.insert_many(records)

print("Data imported successfully!")

client.close()
