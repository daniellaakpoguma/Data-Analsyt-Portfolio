import streamlit as st
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns



# Set the title of your Streamlit app
st.title("Best Social Media")

st.write("DataSet - Which Social Media Millennials Care About Most")
st.write("https://www.kaggle.com/datasets/mawro73/which-social-media-millennials-care-about-most")

# MongoDB connection details
client = MongoClient("mongodb://localhost:27017/")  # Update this with your MongoDB connection string if different
db = client['social_media_data']
collection = db['best_social_media']

# Fetch data from MongoDB
data = list(collection.find())  # Fetch all documents

# Convert the MongoDB documents to a DataFrame
df = pd.DataFrame(data)

# Display the DataFrame in Streamlit
st.dataframe(df)

# Sidebar filters
segment_type_options = df['Segment Type'].unique()
selected_segment_type = st.sidebar.selectbox('Select Segment Type', segment_type_options)

answer_options = df['Answer'].unique()
selected_answer = st.sidebar.selectbox('Select Answer', answer_options)

# Filtered data based on user selection
filtered_data = df[(df['Segment Type'] == selected_segment_type) & (df['Answer'] == selected_answer)]

# Display filtered data
st.write(f"Filtered by Segment Type: {selected_segment_type} and Answer: {selected_answer}")
st.dataframe(filtered_data)


# Group by 'Answer' and aggregate counts and percentages
platform_counts = df.groupby('Answer').agg({
    'Count': 'sum',
    'Percentage': 'mean'  # Assuming 'Percentage' is already in percentage form
}).reset_index()

# Bar plot with counts and percentages
plt.figure(figsize=(12, 8))
sns.barplot(data=platform_counts, x='Answer', y='Count', palette='Set2')
plt.xticks(rotation=45)
plt.xlabel('Social Media Platform')
plt.ylabel('Count')
plt.title('Counts of Social Media Preferences')
plt.tight_layout()


# Adding percentages as text on top of bars
for index, row in platform_counts.iterrows():
    plt.text(index, row['Count'] + 100, f"{row['Count']} ({row['Percentage']:.1%})", ha='center', va='bottom', fontsize=10)

st.pyplot(plt)