import streamlit as st
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string 
import nltk
import warnings
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import requests
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression

warnings.filterwarnings("ignore", category=DeprecationWarning)
nltk.download('punkt')

# Streamlit App
st.title("Twitter Sentiment Analysis")

# Option to use default data or upload files
use_default = st.sidebar.checkbox("Use default dataset")

if use_default:
    train = pd.read_csv('https://raw.githubusercontent.com/dD2405/Twitter_Sentiment_Analysis/master/train.csv')
    test = pd.read_csv('https://raw.githubusercontent.com/dD2405/Twitter_Sentiment_Analysis/master/test.csv')
else:
    # Load data
    st.sidebar.header("Upload CSV Files")
    train_file = st.sidebar.file_uploader("Upload train.csv", type="csv")
    test_file = st.sidebar.file_uploader("Upload test.csv", type="csv")

    if train_file and test_file:
        train = pd.read_csv(train_file)
        test = pd.read_csv(test_file)
    else:
        st.info("Please upload both train.csv and test.csv files.")
        st.stop()

# Display data
st.write("Train Data Head", train.head())
st.write("Test Data Head", test.head())

# Combining the datasets
combined_data = pd.concat([train, test], ignore_index=True, sort=True)
st.write("Combined Data Head", combined_data.head())

# Cleaning Data
def remove_pattern(text, pattern):
    r = re.findall(pattern, text)
    for i in r:
        text = re.sub(i, "", text)
    return text

combined_data['Cleaned_Tweets'] = np.vectorize(remove_pattern)(combined_data['tweet'], "@[\w]*")
combined_data['Cleaned_Tweets'] = combined_data['Cleaned_Tweets'].str.replace("[^a-zA-Z#]", " ")
combined_data['Cleaned_Tweets'] = combined_data['Cleaned_Tweets'].apply(lambda x: ' '.join([w for w in x.split() if len(w) > 3]))

# Tokenization and Stemming
tokenized_tweets = combined_data['Cleaned_Tweets'].apply(lambda x: x.split())
ps = nltk.PorterStemmer()
tokenized_tweets = tokenized_tweets.apply(lambda x: [ps.stem(i) for i in x])
for i in range(len(tokenized_tweets)):
    tokenized_tweets[i] = ' '.join(tokenized_tweets[i])
combined_data['Clean_Tweets'] = tokenized_tweets

# Display cleaned data
st.write("Cleaned Data Head", combined_data.head())

# Data Visualization
positive_words = ' '.join(text for text in combined_data['Clean_Tweets'][combined_data['label'] == 0])
negative_words = ' '.join(text for text in combined_data['Clean_Tweets'][combined_data['label'] == 1])

# Word Cloud for Positive Words
st.subheader("Positive Words Word Cloud")
mask = np.array(Image.open(requests.get('http://clipart-library.com/image_gallery2/Twitter-PNG-Image.png', stream=True).raw))
image_colors = ImageColorGenerator(mask)
wc = WordCloud(background_color='black', height=1500, width=4000, mask=mask).generate(positive_words)
plt.figure(figsize=(15, 30))
plt.imshow(wc.recolor(color_func=image_colors), interpolation="hamming")
plt.axis('off')
st.pyplot(plt.gcf())

# Word Cloud for Negative Words
st.subheader("Negative Words Word Cloud")
wc = WordCloud(background_color='black', height=1500, width=4000, mask=mask).generate(negative_words)
plt.figure(figsize=(15, 30))
plt.imshow(wc.recolor(color_func=image_colors), interpolation="gaussian")
plt.axis('off')
st.pyplot(plt.gcf())

# Extracting Hashtags
def extract_hashtags(x):
    hashtags = []
    for i in x:
        ht = re.findall(r'#(\w+)', i)
        hashtags.append(ht)
    return hashtags

positive_hashTags = extract_hashtags(combined_data['Clean_Tweets'][combined_data['label'] == 0])
negative_hashTags = extract_hashtags(combined_data['Clean_Tweets'][combined_data['label'] == 1])
positive_hastags_unnested = sum(positive_hashTags, [])
negative_hashtags_unnested = sum(negative_hashTags, [])

# Plotting Bar Plots for Hashtags
st.subheader("Hashtag Frequency")

def plot_hashtag_freq(hashtags, label):
    word_freq = nltk.FreqDist(hashtags)
    df = pd.DataFrame({'Hashtags': list(word_freq.keys()), 'Count': list(word_freq.values())})
    df = df.nlargest(20, columns='Count')
    plt.figure(figsize=(15, 8))
    sns.barplot(data=df, y='Hashtags', x='Count')
    sns.despine()
    plt.title(f"Top 20 {label} Hashtags")
    st.pyplot(plt.gcf())

st.write("Positive Hashtags")
plot_hashtag_freq(positive_hastags_unnested, "Positive")
st.write("Negative Hashtags")
plot_hashtag_freq(negative_hashtags_unnested, "Negative")

# Feature Extraction
bow_vectorizer = CountVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words="english")
bow = bow_vectorizer.fit_transform(combined_data['Clean_Tweets'])
tfidf_vectorizer = TfidfVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(combined_data['Clean_Tweets'])

train_bow = bow[:31962]
train_tfidf = tfidf[:31962]

# Splitting data
x_train_bow, x_valid_bow, y_train_bow, y_valid_bow = train_test_split(train_bow, train['label'], test_size=0.3, random_state=2)
x_train_tfidf, x_valid_tfidf, y_train_tfidf, y_valid_tfidf = train_test_split(train_tfidf, train['label'], test_size=0.3, random_state=17)

# Applying ML Models
st.subheader("Model Training and Evaluation")
log_reg = LogisticRegression(random_state=0, solver='lbfgs')

# Logistic Regression with Bag of Words
log_reg.fit(x_train_bow, y_train_bow)
predict_bow = log_reg.predict_proba(x_valid_bow)
prediction_int_bow = predict_bow[:, 1] >= 0.3
prediction_int_bow = prediction_int_bow.astype(int)
log_bow = f1_score(y_valid_bow, prediction_int_bow)
st.write(f"F1 Score (Bag of Words): {log_bow}")

# Logistic Regression with TF-IDF
log_reg.fit(x_train_tfidf, y_train_tfidf)
predict_tfidf = log_reg.predict_proba(x_valid_tfidf)
prediction_int_tfidf = predict_tfidf[:, 1] >= 0.3
prediction_int_tfidf = prediction_int_tfidf.astype(int)
log_tfidf = f1_score(y_valid_tfidf, prediction_int_tfidf)
st.write(f"F1 Score (TF-IDF): {log_tfidf}")

# Final prediction on test data
test_tfidf = tfidf[31962:]
test_pred = log_reg.predict_proba(test_tfidf)
test_pred_int = test_pred[:, 1] >= 0.3
test_pred_int = test_pred_int.astype(int)
test['label'] = test_pred_int
submission = test[['id', 'label']]
submission.to_csv('result.csv', index=False)

# Display results
st.subheader("Prediction Results")
res = pd.read_csv('result.csv')
st.write(res)
