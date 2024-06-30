import os
import pandas as pd
import streamlit as st
from PIL import Image

from pymongo import MongoClient, errors

# Function to connect to MongoDB
def get_mongo_client():
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        client.server_info()  # Trigger exception if cannot connect to the server
        return client
    except errors.ServerSelectionTimeoutError as err:
        st.error("Failed to connect to MongoDB server: {}".format(err))
        return None

# Function to load CSV into MongoDB
def load_csv_to_mongo(file_path, collection_name, db):
    df = pd.read_csv(file_path)
    collection = db[collection_name]
    collection.insert_many(df.to_dict('records'))

# Function to fetch data from MongoDB and convert to DataFrame
def fetch_data(collection_name, limit=5, db=None):
    collection = db[collection_name]
    data = collection.find().limit(limit)
    df = pd.DataFrame(list(data))
    return df

# List of CSV files and their corresponding collections
csv_files = {
    "Facebook -  Posts.csv": "Facebook_Posts",
    "Facebook -  Comments.csv": "Facebook_Comments",
    "Instagram - Profiles.csv": "Instagram_Profiles",
    "Instagram - Posts.csv": "Instagram_Posts",
    "Instagram - Comments.csv": "Instagram_Comments",
    "Pinterest - Profiles.csv": "Pinterest_Profiles",
    "Pinterest - Posts .csv": "Pinterest_Posts",
    "TikTok - Profiles.csv": "Tiktok_Profiles",
    "TikTok - Posts.csv": "Tiktok_Posts",
    "TikTok - Comments.csv": "Tiktok_Comments",
    "YouTube - Profiles.csv": "Youtube_Profiles",
    "Youtube - Videos posts.csv": "Youtube_Posts",
    "Youtube - Comments.csv": "Youtube_Comments"
}

# Main Streamlit application
def main():
    st.title("Data Sets")

    st.markdown("""## Social Media Data""")

    # Load data directly from local CSV files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))  # One level up
    
    for relative_path, collection_name in csv_files.items():
        absolute_path = os.path.join(parent_dir, relative_path)
        
        if os.path.exists(absolute_path):
            df = pd.read_csv(absolute_path)
            # Dynamically create DataFrame variables
            globals()[f'df_{collection_name}'] = df
        else:
            st.error(f"File not found: {absolute_path}")

    # Display data for each platform and data type
    st.subheader("Facebook")
    st.subheader("Posts")
    if 'df_Facebook_Posts' in globals():
        st.dataframe(df_Facebook_Posts.head(10))

    st.subheader("Comments")
    if 'df_Facebook_Comments' in globals():
        st.dataframe(df_Facebook_Comments.head(10))

    st.subheader("Instagram")
    st.subheader("Profiles")
    if 'df_Instagram_Profiles' in globals():
        st.dataframe(df_Instagram_Profiles.head(10))

    st.subheader("Posts")
    if 'df_Instagram_Posts' in globals():
        st.dataframe(df_Instagram_Posts.head(10))

    st.subheader("Comments")
    if 'df_Instagram_Comments' in globals():
        st.dataframe(df_Instagram_Comments.head(10))

    st.subheader("Pinterest")
    st.subheader("Profiles")
    if 'df_Pinterest_Profiles' in globals():
        st.dataframe(df_Pinterest_Profiles.head(10))

    st.subheader("Posts")
    if 'df_Pinterest_Posts' in globals():
        st.dataframe(df_Pinterest_Posts.head(10))

    st.subheader("TikTok")
    st.subheader("Profiles")
    if 'df_Tiktok_Profiles' in globals():
        st.dataframe(df_Tiktok_Profiles.head(10))

    st.subheader("Posts")
    if 'df_Tiktok_Posts' in globals():
        st.dataframe(df_Tiktok_Posts.head(10))

    st.subheader("Comments")
    if 'df_Tiktok_Comments' in globals():
        st.dataframe(df_Tiktok_Comments.head(10))

    st.subheader("YouTube")
    st.subheader("Profiles")
    if 'df_Youtube_Profiles' in globals():
        st.dataframe(df_Youtube_Profiles.head(10))

    st.subheader("Posts")
    if 'df_Youtube_Posts' in globals():
        st.dataframe(df_Youtube_Posts.head(10))

    st.subheader("Comments")
    if 'df_Youtube_Comments' in globals():
        st.dataframe(df_Youtube_Comments.head(10))

    st.markdown("""##  Social Media Advertisement Data""")

    st.write("1. Revenue of Advertising in US:")
    st.write("https://www.statista.com/statistics/269916/mobile-advertising-spending-in-the-united-states/")
    st.write("2. Social Networking - Worldwide:")
    st.write("https://www.statista.com/outlook/amo/app/social-networking/worldwide")

    st.markdown("""##  Social Media ML Analysis""")
    # Get the directory of the current script
    st.markdown("1. <u>Machine learning algorithms for social media analysis: A survey</u>", unsafe_allow_html=True)
    st.write("""This article is just a more general one, providing insights into various applications of SM analysis: 
             anomaly detection, behavioral analysis, bioinformatics, business intelligence, crime detection, epidemics,
             event detection, image analysis, recommendations, relationships, and reputations,
            and sentiment, opinion and emotions analysis""")
    st.write("https://www.sciencedirect.com/science/article/abs/pii/S1574013721000356")
    st.markdown("2. <u> A Study on Machine Learning in Social Media</u>", unsafe_allow_html=True)
    st.write("https://www.ijser.org/researchpaper/A-Study-on-Machine-Learning-in-Social-Media.pdf")
    st.markdown("3. <u> How well can machine learning predict demographics of social media users? </u>", unsafe_allow_html=True)
    st.write(""" This article talks more about using social media used to study huuman behvaiour """)
    st.write("https://www.ijser.org/researchpaper/A-Study-on-Machine-Learning-in-Social-Media.pdf")

   
   

# Run the main function
if __name__ == "__main__":
    main()
