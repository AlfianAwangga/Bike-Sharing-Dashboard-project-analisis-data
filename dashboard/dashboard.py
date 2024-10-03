import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style="dark")

#Fungsi Workingday vs Holiday
def create_holiday_df(df):
    holiday_df = df[df["holiday"] == 1]
    return holiday_df

def create_workingday_df(df):
    workingday_df = df[df["workingday"] == 1]
    return workingday_df

def average_rent_on_holiday(df):
    average_rent_on_holiday = df.cnt.mean()
    return average_rent_on_holiday

def average_rent_on_workingday(df):
    average_rent_on_workingday = df.cnt.mean()
    return average_rent_on_workingday

def merge_holiday_workingday_df(av1, av2):
    holiday_vs_workingday_df = pd.DataFrame({
        "category": ["Holiday", "Workingday"],
        "average_rents": [av1, av2]
    })
    return holiday_vs_workingday_df

# Fungsi Korelasi Cuaca
def create_by_windspeed_df(df):
    by_windspeed_df = df.groupby("windspeed").agg({
        "cnt": "sum"
    })
    by_windspeed_df.rename(columns={
        "cnt": "bike_rentals"
    }, inplace=True)
    by_windspeed_df["windspeed_kmh"] = by_windspeed_df.index*67
    return by_windspeed_df

def create_by_hum_df(df):
    by_hum_df = df.groupby("hum").agg({
        "cnt": "sum"
    })
    by_hum_df.rename(columns={
        "cnt": "bike_rentals"
    }, inplace=True)
    by_hum_df["hum_percent"] = by_hum_df.index*100
    return by_hum_df

hour_df = pd.read_csv("dashboard/hour.csv")
day_df = pd.read_csv("dashboard/day.csv")

workingday_df = create_workingday_df(day_df)
holiday_df = create_holiday_df(day_df)
average_holiday = average_rent_on_holiday(holiday_df)
average_workingday = average_rent_on_workingday(workingday_df)
holiday_vs_workingday_df = merge_holiday_workingday_df(average_holiday, average_workingday)

by_windspeed_df = create_by_windspeed_df(hour_df)
by_hum_df = create_by_hum_df(hour_df)

st.header("Bike-Sharing Dashboard 🚲")
st.subheader("Working day vs Holiday")

with st.sidebar:
    list = ["Working day vs Holiday", "Weather Impact on Bike Rentals"]
    st.header("Bike-Sharing Dashboard 🚲")
    for x in list:
        st.write(x)
    st.caption("Alfian Diva Awangga")

# Metrik Workingday vs Holiday
col1, col2 = st.columns(2)
with col1:
    st.metric(
        "Avg. Bike Rentals on Workingday :", 
        value=average_workingday
    )

with col2:
    st.metric(
        "Avg. Bike Rentals on Holiday :", 
        value=average_holiday
    )

# Bar Chart Workingday vs Holiday
fig, ax = plt.subplots(figsize=(20,10))
colors = ["blue", "red"]

sns.barplot(
    x="category",
    y="average_rents",
    data=holiday_vs_workingday_df.sort_values(by="average_rents", ascending=False),
    palette=colors,
    width=0.65,
    ax=ax
)
ax.set_title("Average Bike Rentals on Working Day vs Holiday", fontsize=30)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis="x", labelsize=30)
ax.tick_params(axis="y", labelsize=25)
st.pyplot(fig)

# Line Chart Kecepatan Angin dan Kelembaban
st.subheader("Weather Impact on Bike Rentals")

# Metrik Kecepatan Angin
corr_windspeed = by_windspeed_df["windspeed_kmh"].corr(by_windspeed_df["bike_rentals"])
st.metric(
    "Corr. Windspeed - Bike Rentals :",
    value=round(corr_windspeed, 2)
)

#Line Chart Kecepatan Angin
fig, ax = plt.subplots(figsize=(20,10))

sns.lineplot(
    x="windspeed_kmh",
    y="bike_rentals",
    data=by_windspeed_df,
    color="blue",
    linewidth=3,
    ax=ax
)
ax.set_title("Correlation between Wind Speed ​​and Number of Bicycle Rentals", fontsize=30)
ax.set_xlabel("Windspeed (Km/h)", fontsize=25)
ax.set_ylabel("Bike Rentals (Unit)", fontsize=25)
ax.tick_params(axis="x", labelsize=20)
ax.tick_params(axis="y", labelsize=20)
st.pyplot(fig)

# Metrik Kelembaban
corr_hum = by_hum_df["hum_percent"].corr(by_hum_df["bike_rentals"])
st.metric(
    "Corr. Humidity - Bike Rentals :",
    value=round(corr_hum, 2)
)

# Line Chart Kelembaban
fig, ax = plt.subplots(figsize=(20,10))

sns.lineplot(
    x="hum_percent",
    y="bike_rentals",
    data=by_hum_df,
    color="orange",
    linewidth=3,
    ax=ax
)
ax.set_title("Correlation between Humidity ​​and Number of Bicycle Rentals", fontsize=30)
ax.set_xlabel("Humidity (%)", fontsize=25)
ax.set_ylabel("Bike Rentals (Unit)", fontsize=25)
ax.tick_params(axis="x", labelsize=20)
ax.tick_params(axis="y", labelsize=20)
st.pyplot(fig)


