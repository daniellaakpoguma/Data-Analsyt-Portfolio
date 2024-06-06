import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt
import os

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Navigate up one directory level from the script's location (equivalent to removing 'pages')
base_dir = os.path.dirname(script_dir)

# Construct the relative path to the CSV file
file_path = os.path.join(base_dir, 'AQI and Lat Long of Countries.csv')
# Read the Excel file
df = pd.read_csv(file_path)

# Drop rows with missing or invalid values in the 'mag' column
df = df.dropna(subset=['AQI Value'])
df = df[df['AQI Value'] >= 0]

# Create scatter map
fig = px.scatter_geo(df, lat='lat', lon='lng', color='AQI Value',
                     hover_name='City', # Add more hover data if needed
                     title='Air Quality Index (AQI) Across Cities')
fig.show()


st.plotly_chart(fig)