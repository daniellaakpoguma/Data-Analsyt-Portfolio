import os
import pandas as pd
import pymongo
import streamlit as st

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["reviews"]  # This creates the database if it doesn't exist
collection = db["mcdonalds"] # This creates the collection if it doesn't exist

# Insert DataFrame into MongoDB (run once to insert data)
if collection.count_documents({}) == 0:  # Check if collection is empty
    script_dir = os.path.dirname(__file__)
    base_dir = os.path.dirname(script_dir)
    file_path = os.path.join(base_dir, 'McDonald_s_Reviews.csv')
    df = pd.read_csv(file_path, encoding='latin-1')
    collection.insert_many(df.to_dict('records'))

# Fetch data from MongoDB
data = list(collection.find({}, {'_id': False}))  # Exclude the '_id' field
df_from_db = pd.DataFrame(data)

# Streamlit app
st.title("Data from MongoDB")

if not df_from_db.empty:
    st.write(df_from_db)
else:
    st.write("No data found.")
