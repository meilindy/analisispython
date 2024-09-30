import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set the style for seaborn
sns.set(style='dark')

# Helper function to create specific DataFrames for analysis
def create_temp_polutant_df(df):
    temp_polutant_df = df[['TEMP', 'PM2.5', 'CO', 'O3']]
    return temp_polutant_df.corr()

def create_precipitation_wind_df(df):
    precipitation_wind_df = df[['PRES', 'WSPM']].dropna()
    return precipitation_wind_df

def create_avg_temp_per_month_df(df):
    df['month'] = pd.to_datetime(df['month'], format='%m')
    avg_temp_per_month = df.groupby(df['month'].dt.month)['TEMP'].mean().reset_index()
    avg_temp_per_month['month'] = avg_temp_per_month['month'].apply(lambda x: f'Month {x}')
    return avg_temp_per_month

# Load dataset
air_quality_df = pd.read_csv("df.csv")

# Create a 'date' column in the dataframe
air_quality_df["date"] = pd.to_datetime(air_quality_df["year"].astype(str) + '-' + air_quality_df["month"].astype(str) + '-' + air_quality_df["day"].astype(str))

# Sidebar options
min_date = air_quality_df["date"].min()
max_date = air_quality_df["date"].max()

# Sidebar logo and date range selection
with st.sidebar:
    st.image("logo.jpg")
    start_date, end_date = st.date_input('Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date])

# Convert start_date and end_date to pandas Timestamp
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter the dataset based on the selected date range
filtered_data = air_quality_df[(air_quality_df["date"] >= start_date) & (air_quality_df["date"] <= end_date)]

# Create dataframes for visualization
temp_polutant_corr = create_temp_polutant_df(filtered_data)
precipitation_wind_df = create_precipitation_wind_df(filtered_data)
avg_temp_per_month = create_avg_temp_per_month_df(filtered_data)

# Main title
st.header('Air Quality Dashboard :sparkles:')

# Correlation between Temperature and Pollutants
st.subheader('Correlation between Temperature and Pollutants (PM2.5, CO, O3)')

fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(temp_polutant_corr, annot=True, cmap="coolwarm", ax=ax)
plt.title("Correlation Heatmap", loc="center", fontsize=15)
st.pyplot(fig)

# Scatterplot Correlation between Temperature and Pollutants
st.subheader('Scatterplot Correlation between Temperature and Pollutants (PM2.5, CO, O3)')

fig, axs = plt.subplots(3, 1, figsize=(20, 10))
sns.scatterplot(ax=axs[0], x='TEMP', y='PM2.5', data=filtered_data, label='PM2.5')
sns.scatterplot(ax=axs[1], x='TEMP', y='CO', data=filtered_data, label='CO')
sns.scatterplot(ax=axs[2], x='TEMP', y='O3', data=filtered_data, label='O3')
plt.legend()
st.pyplot(fig)

# Scatter plot between Precipitation and Wind Speed
st.subheader('Scatter Plot: Precipitation vs Wind Speed')

fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x='PRES', y='WSPM', data=precipitation_wind_df, ax=ax)
plt.title("Precipitation vs Wind Speed", loc="center", fontsize=15)
plt.xlabel("Precipitation")
plt.ylabel("Wind Speed (WSPM)")
st.pyplot(fig)

# Bar plot of Precipitation binned by Wind Speed
air_quality_df['WSPM_binned'] = pd.cut(air_quality_df['WSPM'], bins=10)

st.subheader('Bar Plot of Precipitation Binned by Wind Speed')
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(y="PRES", x="WSPM_binned", data=air_quality_df, ax=ax)
plt.xticks(rotation=45)  # Rotate labels for better readability
st.pyplot(fig)

# Line plot of Average Temperature per Month
st.subheader('Average Temperature per Month')

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='month', y='TEMP', data=avg_temp_per_month, ax=ax)
plt.title("Average Temperature per Month", loc="center", fontsize=15)
plt.xlabel("Month")
plt.ylabel("Average Temperature (°C)")
plt.tick_params(axis='x', labelsize=12)
plt.xticks(rotation=45)
st.pyplot(fig)
