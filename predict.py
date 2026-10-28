import os
import joblib
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

model = joblib.load("solar_model.pkl")

client = MongoClient(os.getenv("MONGO_URI"))
db = client["solar_power_db"]

irradiation = float(input("Enter irradiation: "))
ambient = float(input("Enter ambient temperature: "))
module = float(input("Enter module temperature: "))
hour = int(input("Enter hour (0-23): "))
month = int(input("Enter month (1-12): "))

data = pd.DataFrame([{
    "IRRADIATION": irradiation,
    "AMBIENT_TEMPERATURE": ambient,
    "MODULE_TEMPERATURE": module,
    "HOUR": hour,
    "MONTH": month
}])

prediction = model.predict(data)[0]
prediction = max(0, prediction)

print("Predicted AC Power:", round(prediction, 2), "kW")

db.predictions.insert_one({
    "IRRADIATION": irradiation,
    "AMBIENT_TEMPERATURE": ambient,
    "MODULE_TEMPERATURE": module,
    "HOUR": hour,
    "MONTH": month,
    "PREDICTED_AC_POWER": round(float(prediction), 2)
})

print("Prediction saved to MongoDB!")
client.close()
