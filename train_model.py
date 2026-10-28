import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

data = pd.read_csv("merged_solar_data.csv")


data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"], dayfirst=True)
data["HOUR"] = data["DATE_TIME"].dt.hour
data["MONTH"] = data["DATE_TIME"].dt.month


features = [
    "IRRADIATION",
    "AMBIENT_TEMPERATURE",
    "MODULE_TEMPERATURE",
    "HOUR",
    "MONTH"
]

target = "AC_POWER"


data = data.dropna(subset=features + [target])
data = data[data["IRRADIATION"] >= 0]

X = data[features]
y = data[target]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


model = LinearRegression()
model.fit(X_train, y_train)


predictions = model.predict(X_test)


mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print("Training completed!")
print(f"Training records: {len(X_train)}")
print(f"Testing records: {len(X_test)}")
print(f"R² Score: {r2:.4f}")
print(f"MAE: {mae:.4f} kW")
print(f"RMSE: {rmse:.4f} kW")


import joblib
joblib.dump(model, "solar_model.pkl")
print("Model saved as solar_model.pkl")