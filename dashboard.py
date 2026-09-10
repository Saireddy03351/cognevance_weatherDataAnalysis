import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Hyderabad Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# Load data
df = pd.read_csv("weather_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

# -------------------------
# TITLE
# -------------------------
st.title("🌤️ Hyderabad Weather Analysis Dashboard")
st.markdown("### Interactive Weather Data Analysis")

# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.header("🔍 Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    df["Date"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Date"].max().date()
)

weather_options = ["All"] + sorted(df["Weather"].unique().tolist())

selected_weather = st.sidebar.selectbox(
    "Weather Condition",
    weather_options
)

# -------------------------
# FILTER DATA
# -------------------------
filtered_df = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date)
]

if selected_weather != "All":
    filtered_df = filtered_df[
        filtered_df["Weather"] == selected_weather
    ]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# -------------------------
# KEY METRICS
# -------------------------
st.subheader("📌 Key Weather Statistics")

avg_temp = filtered_df["Temperature_C"].mean()
avg_humidity = filtered_df["Humidity_pct"].mean()
avg_wind = filtered_df["Wind_Speed_kmh"].mean()
total_rain = filtered_df["Precipitation_mm"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌡️ Avg Temperature", f"{avg_temp:.2f} °C")
col2.metric("💧 Avg Humidity", f"{avg_humidity:.2f} %")
col3.metric("💨 Avg Wind Speed", f"{avg_wind:.2f} km/h")
col4.metric("🌧️ Total Rainfall", f"{total_rain:.2f} mm")

# -------------------------
# TEMPERATURE CHART
# -------------------------
st.subheader("🌡️ Temperature Trend")

st.line_chart(
    filtered_df.set_index("Date")["Temperature_C"]
)

# -------------------------
# HUMIDITY CHART
# -------------------------
st.subheader("💧 Humidity Trend")

st.line_chart(
    filtered_df.set_index("Date")["Humidity_pct"]
)

# -------------------------
# RAINFALL + WEATHER
# -------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌧️ Rainfall")

    st.bar_chart(
        filtered_df.set_index("Date")["Precipitation_mm"]
    )

with col2:
    st.subheader("☀️ Weather Conditions")

    weather_count = filtered_df["Weather"].value_counts()

    fig, ax = plt.subplots()
    ax.pie(
        weather_count.values,
        labels=weather_count.index,
        autopct="%1.1f%%"
    )
    ax.set_title("Weather Condition Distribution")

    st.pyplot(fig)

# -------------------------
# DATA TABLE
# -------------------------
st.subheader("📋 Weather Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# -------------------------
# DOWNLOAD DATA
# -------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_weather_data.csv",
    mime="text/csv"
)
# -------------------------
# DATA INSIGHTS
# -------------------------
st.subheader("💡 Key Insights")

highest_temp = filtered_df.loc[
    filtered_df["Temperature_C"].idxmax()
]

lowest_temp = filtered_df.loc[
    filtered_df["Temperature_C"].idxmin()
]

highest_rain = filtered_df.loc[
    filtered_df["Precipitation_mm"].idxmax()
]

most_common_weather = filtered_df["Weather"].mode()[0]

st.write(
    f"🌡️ Highest temperature was "
    f"**{highest_temp['Temperature_C']} °C** "
    f"on **{highest_temp['Date'].strftime('%d-%m-%Y')}**."
)

st.write(
    f"❄️ Lowest temperature was "
    f"**{lowest_temp['Temperature_C']} °C** "
    f"on **{lowest_temp['Date'].strftime('%d-%m-%Y')}**."
)

st.write(
    f"🌧️ Highest rainfall was "
    f"**{highest_rain['Precipitation_mm']} mm** "
    f"on **{highest_rain['Date'].strftime('%d-%m-%Y')}**."
)

st.write(
    f"☀️ The most common weather condition was "
    f"**{most_common_weather}**."
)
st.success("Weather analysis completed successfully! ✅")