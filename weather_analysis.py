import pandas as pd

# Load dataset
df = pd.read_csv("weather_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Calculate key statistics
avg_temp = df["Temperature_C"].mean()
avg_humidity = df["Humidity_pct"].mean()
avg_wind = df["Wind_Speed_kmh"].mean()
total_rain = df["Precipitation_mm"].sum()
max_temp = df["Temperature_C"].max()
min_temp = df["Temperature_C"].min()

print("=" * 45)
print("       WEATHER ANALYSIS REPORT")
print("=" * 45)

print(f"Location: {df['Location'].iloc[0]}")
print(f"Total Days: {len(df)}")

print("\n--- Key Statistics ---")
print(f"Average Temperature : {avg_temp:.2f} °C")
print(f"Average Humidity    : {avg_humidity:.2f} %")
print(f"Average Wind Speed  : {avg_wind:.2f} km/h")
print(f"Total Rainfall     : {total_rain:.2f} mm")
print(f"Maximum Temperature: {max_temp} °C")
print(f"Minimum Temperature: {min_temp} °C")

print("\n--- Weather Conditions ---")
print(df["Weather"].value_counts())

print("\n--- Analysis Completed Successfully ---")