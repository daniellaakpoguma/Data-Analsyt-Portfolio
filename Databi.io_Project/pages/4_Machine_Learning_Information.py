import streamlit as st
import pandas as pd
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


st.title("Machine Learning Models")

st.write("""
1. **Sentiment Analysis**
**Useful Information:**
- **Post Content:** Text of posts and articles.
- **Comments:** User comments on posts.
- **Direct Messages (DMs):** Messages between users (if accessible and compliant with privacy policies).
- **Company Reviews:** Reviews and feedback about companies.

**Example Features:**
- Text data (processed with tokenization, stop-word removal, etc.).
- Sentiment scores (positive, negative, neutral).
- Word frequency, bigrams, trigrams.

2. **Topic Modeling**
**Useful Information:**
- **Post Content:** Text of posts and articles.
- **Comments:** User comments on posts.
- **Job Descriptions:** Text of job postings.

**Example Features:**
- Text data (processed and cleaned).
- Frequency of words and phrases.
- Term-document matrix for LDA.

3. **User Segmentation**
**Useful Information:**
- **User Profiles:** Job titles, industries, locations, skills.
- **Engagement Metrics:** Likes, comments, shares, views.
- **Activity Data:** Frequency of posting, type of content posted.

**Example Features:**
- Engagement rates (e.g., likes per post, comments per post).
- Profile features (e.g., job title, industry, location).
- Posting frequency.
- Follower/following ratio.
- Clustering features (e.g., k-means input features).

4. **Engagement Prediction**
**Features:** 
-content
-hashtags
-page_name
-date_posted
**Target:** 
-num_of_comment
-num_of_likes
-num_of_shares
         Model: Regression models (e.g., linear regression, random forest regressor, neural networks)

5. **Recommendation Systems**
**Useful Information:**
- **User Interactions:** Likes, comments, shares, follows, connections.
- **Content Data:** Posts, articles, job listings.
- **User Profiles:** User skills, job titles, interests.

**Example Features:**
- User-item interaction matrix.
- Content features (e.g., text embeddings, image embeddings).
- Collaborative filtering features (e.g., user-user similarity).

6. **Trend Analysis**
**Useful Information:**
- **Engagement Metrics:** Time-series data of likes, comments, shares.
- **Post Data:** Content posted over time (text, images, videos).
- **Skills and Endorsements:** Trends in skill endorsements.

**Example Features:**
- Time-series features (e.g., daily/weekly engagement metrics).
- Seasonal patterns.
- Content trends over time.

7. **Automated Content Generation**
**Useful Information:**
- **Post Data:** Successful posts (high engagement) and their attributes.
- **Articles:** Examples of engaging articles.
- **Job Descriptions:** Examples of effective job postings.

**Example Features:**
- Text data from high-engagement posts.
- NLP features (e.g., language models for text generation).
- Image features for generating visually appealing content.
""")


# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']

# Function to fetch data from MongoDB and convert to DataFrame
def fetch_data(collection_name, limit=100, db=None):
    collection = db[collection_name]
    data = collection.find().limit(limit)
    df = pd.DataFrame(list(data))
    return df

# Title of the application
st.title("Instagram Post Engagement Predictor")

# Fetch data from MongoDB
df_posts = fetch_data('Instagram_Posts', db=db)

# Display the data
st.subheader("Instagram Posts Data")
st.dataframe(df_posts.head(10))

# Select features and target
st.write("Select Features and Target")
all_columns = df_posts.columns.tolist()
features = st.multiselect("Select Features", all_columns, default=['num_comments', 'likes', 'photos', 'videos', 'video_view_count', 'video_play_count'])
target = st.selectbox("Select Target", ['engagement_score_view'])

if len(features) > 0 and target:
    # Prepare the data
    X = df_posts[features]
    y = df_posts[target]

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Display evaluation metrics
    st.write(f"Mean Squared Error: {mse}")
    st.write(f"R^2 Score: {r2}")

    # Visualize the results
    st.write("Actual vs Predicted")
    results = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})
    st.line_chart(results)
else:
    st.write("Please select at least one feature and a target.")