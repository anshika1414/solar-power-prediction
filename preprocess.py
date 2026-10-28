import pandas as pd

generation = pd.read_csv("Plant_1_Generation_Data.csv")
weather = pd.read_csv("Plant_1_Weather_Sensor_Data.csv")

print("Generation dataset shape:", generation.shape)
print("Weather dataset shape:", weather.shape)

print("\nGeneration columns:")
print(generation.columns.tolist())

print("\nWeather columns:")
print(weather.columns.tolist())


generation["DATE_TIME"] = pd.to_datetime(generation["DATE_TIME"])
weather["DATE_TIME"] = pd.to_datetime(weather["DATE_TIME"])


data = pd.merge(
    generation,
    weather,
    on="DATE_TIME",
    how="inner"
)

print("\nMerged dataset shape:", data.shape)
print("\nFirst 5 rows:")
print(data.head())

print("\nMissing values:")
print(data.isnull().sum())

print("\nDuplicate rows:", data.duplicated().sum())


data.to_csv("merged_solar_data.csv", index=False)
print("\nMerged dataset saved successfully!")
