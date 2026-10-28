import os
import joblib
import pandas as pd
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

model = joblib.load("solar_model.pkl")
client = MongoClient(os.getenv("MONGO_URI"))
db = client["solar_power_db"]

st.set_page_config(page_title="Solar Power Prediction", page_icon="☀️")

st.title("☀️ Solar Power Prediction System")
st.write("Predict solar power using weather conditions.")

st.subheader("Enter Weather Conditions")

irradiation = st.number_input(
    "Solar Irradiation", min_value=0.0, value=0.5
)
ambient = st.number_input(
    "Ambient Temperature (°C)", value=25.0
)
module = st.number_input(
    "Module Temperature (°C)", value=30.0
)
hour = st.slider("Hour of Day", 0, 23, 12)
month = st.slider("Month", 1, 12, 5)

if st.button("Predict Solar Power"):
    data = pd.DataFrame([{
        "IRRADIATION": irradiation,
        "AMBIENT_TEMPERATURE": ambient,
        "MODULE_TEMPERATURE": module,
        "HOUR": hour,
        "MONTH": month
    }])

    prediction = max(0, float(model.predict(data)[0]))

    st.success(f"Predicted AC Power: {prediction:.2f} kW")

    db.predictions.insert_one({
        "IRRADIATION": irradiation,
        "AMBIENT_TEMPERATURE": ambient,
        "MODULE_TEMPERATURE": module,
        "HOUR": hour,
        "MONTH": month,
        "PREDICTED_AC_POWER": prediction
    })

    st.info("Prediction saved to MongoDB!")

st.divider()
st.subheader("Previous Predictions")

records = list(
    db.predictions.find(
        {},
        {"_id": 0}
    )
)

if records:
    df = pd.DataFrame(records)

    st.dataframe(df, use_container_width=True)

    chart_df = pd.DataFrame({
        "Prediction Number": range(1, len(df) + 1),
        "Predicted AC Power (kW)": df["PREDICTED_AC_POWER"].values
    })

    st.line_chart(
        chart_df,
        x="Prediction Number",
        y="Predicted AC Power (kW)",
        x_label="Prediction Number",
        y_label="Predicted AC Power (kW)"
    )
else:
    st.write("No predictions available yet.")

client.close()
