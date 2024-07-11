import streamlit as st

st.title("Useful Information for Machine Learning Models on LinkedIn Data")

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
**Useful Information:**
- **Post Content:** Text, images, videos, hashtags.
- **Historical Engagement Data:** Number of likes, comments, shares for past posts.
- **User Activity:** Frequency of posting, types of posts.

**Example Features:**
- Post content features (e.g., text embeddings, image embeddings).
- Historical engagement metrics.
- Time of posting.
- User profile features (e.g., number of connections, job title).

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
