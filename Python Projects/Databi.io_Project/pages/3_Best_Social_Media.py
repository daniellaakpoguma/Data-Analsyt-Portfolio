import streamlit as st
import pandas as pd
from pymongo import MongoClient

# Set the title of your Streamlit app
st.title("Best Social Media")

st.write("DataSet - Which Social Media Millennials Care About Most")
st.write("https://www.kaggle.com/datasets/mawro73/which-social-media-millennials-care-about-most")


# MongoDB connection details
client = MongoClient("mongodb://localhost:27017/")  # Update this with your MongoDB connection string if different
db = client['social_media_data']
collection = db['best_social_media']

# Fetch data from MongoDB
data = list(collection.find().limit(10))  # Fetch the first 10 documents

# Convert the MongoDB documents to a DataFrame
df = pd.DataFrame(data)

# Display the DataFrame in Streamlit
st.dataframe(df)


