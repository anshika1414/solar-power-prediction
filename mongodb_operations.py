
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["solar_power_db"]
collection = db["predictions"]

#create: Inserting a prediction
result = collection.insert_one({
    "IRRADIATION": 0.5,
    "PREDICTED_AC_POWER": 624.63
})
print("Inserted:", result.inserted_id)

#read: Displaying predictions
for record in collection.find():
    print(record)

#update: Change the predicted power
collection.update_one(
    {"_id": result.inserted_id},
    {"$set": {"PREDICTED_AC_POWER": 650.0}}
)
print("Prediction updated")

#delete: Removing this test prediction
collection.delete_one({"_id": result.inserted_id})
print("Test prediction deleted")

#aggregation: Calculate average predicted power
pipeline = [
    {"$group": {
        "_id": None,
        "average_power": {"$avg": "$PREDICTED_AC_POWER"},
        "maximum_power": {"$max": "$PREDICTED_AC_POWER"}
    }}
]
print("Statistics:", list(collection.aggregate(pipeline)))

#indexing: Speed up queries on irradiation
collection.create_index("IRRADIATION")
print("Index created")

client.close()
