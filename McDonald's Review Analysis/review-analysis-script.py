import pandas as pd
import os
from dateutil import parser
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# download nltk corpus (first time only)
# nltk.download('all')

def parse_relative_date(time_string):
     # Get the current date
    current_date = datetime(2023, 1, 1)

     # Handle different time descriptions
    if 'month' in time_string:
        number = int(time_string.split()[0]) if time_string.split()[0].isdigit() else 1
        return current_date - relativedelta(months=number)
    elif 'year' in time_string:
        number = int(time_string.split()[0]) if time_string.split()[0].isdigit() else 1
        return current_date - relativedelta(years=number)
    elif 'day' in time_string:
        number = int(time_string.split()[0]) if time_string.split()[0].isdigit() else 1
        return current_date - relativedelta(days=number)
    elif 'week' in time_string:
        number = int(time_string.split()[0]) if time_string.split()[0].isdigit() else 1
        return current_date - relativedelta(weeks=number)
    else:
        # Return current date if format is not recognized
        return current_date

def parse_rating(rating_str):
    parts = rating_str.split(' ')
    rating_int = parts[0]
    return int(rating_int)

# Function to split address into components
def split_address(address):
    # Split by comma
    parts = address.split(', ')
    
    # Initialize variables with None
    street_address = city = state = postal_code = country = None
    
    # Ensure we have at least 4 parts (street, city, state+postal, country)
    if len(parts) >= 4:
        # Extract the last part as country
        country = parts[-1].strip()
        
        # Extract the third part from the end as state and postal code
        state_zip = parts[-2].strip()
        state_zip_parts = state_zip.split(' ')
        state = state_zip_parts[0].strip() if len(state_zip_parts) > 0 else None
        postal_code = state_zip_parts[1].strip() if len(state_zip_parts) > 1 else None
        
        # Extract the second part from the end as city
        city = parts[-3].strip()
        
        # All parts before these are considered part of the street address
        street_address = ', '.join(parts[:-3]).strip()
    
    return pd.Series([street_address, city, state, postal_code, country],
                     index=['street_address', 'city', 'state', 'zip_code', 'country'])

# create preprocess_text function
def preprocess_text(text):

    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove stop words
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]

    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    # Join the tokens back into a string
    processed_text = ' '.join(lemmatized_tokens)

    return processed_text

def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    pos_score = scores['pos'] 
    if pos_score >= 0.7:
        sentiment = "Strongly Positive"
    elif pos_score >= 0.5:
        sentiment = "Positive"
    elif pos_score > -0.5:
        sentiment = "Neutral"
    elif pos_score > -0.7:
        sentiment = "Negative"
    else:
        sentiment = "Strongly Negative"   
    return scores['score'], sentiment

# Get file path
file_path = r"C:\Users\rukev\OneDrive\Desktop\Data Analsyt Portfolio\Data-Analsyt-Portfolio\Data Sets\McDonald's Store Reviews\McDonald_s_Reviews.csv"

# Read file into single dataframe
try:
    reviews_df = pd.read_csv(file_path, encoding='latin1')
    print(reviews_df.head())
    print(reviews_df.info())           
    print(reviews_df.describe())  

    # Checking for missing values
    print("Before checking for missing values:")
    print(reviews_df.isnull().sum())

    # Dropping Latitude and Longitude Columns
    # Added category and store_name because it is the same information for all columns
    to_drop = ['latitude ','longitude', 'store_name', 'category']
    reviews_df.drop(columns=to_drop, inplace=True)

    print("After handling missing values:")
    print(reviews_df.isnull().sum())

    print("Before removing duplicates:", reviews_df.shape)
    reviews_df_nomissing_unique = reviews_df.drop_duplicates()
    print("After removing duplicates:", reviews_df_nomissing_unique.shape)

    # Remove White Space for column names
    reviews_df_nomissing_unique.columns = reviews_df_nomissing_unique.columns.str.strip()
    reviews_df_nomissing_unique = reviews_df_nomissing_unique.map(lambda x: x.strip() if isinstance(x, str) else x)

    # Setting Reviewe Id to the index
    print(reviews_df_nomissing_unique['reviewer_id'].is_unique) # Check if it is unique
    reviews_df_nomissing_unique = reviews_df_nomissing_unique.set_index('reviewer_id')

    # Split Address to different columns
    reviews_df_nomissing_unique[['street_address', 'city', 'state', 'zip_code', 'country']] = reviews_df_nomissing_unique['store_address'].apply(split_address)

    # Drop Store Address column
    reviews_df_nomissing_unique.drop(columns=['store_address'], inplace=True)

    print("After formatting:")
    print(reviews_df_nomissing_unique.head())
    print("New columns:")
    print(reviews_df_nomissing_unique[['street_address', 'city', 'state', 'zip_code', 'country']])

    # See Dinstict valuesin street address table
    for column in ['street_address', 'city', 'state', 'zip_code', 'country']:
        distinct_values = reviews_df_nomissing_unique[column].unique()
        print(f"Distinct values in {column}:")
        print(distinct_values)
        print()

    # Dictionary to map state abbreviations to full names
    state_mapping = {
        'TX': 'Texas',
        'PA': 'Pennsylvania',
        'NY': 'New York',
        'DC': 'District of Columbia',
        'CA': 'California',
        'FL': 'Florida',
        'UT': 'Utah',
        'IL': 'Illinois',
        'NJ': 'New Jersey',
        'NV': 'Nevada',
        'VA': 'Virginia'
    }

    # Replace abbreviations with full state names
    reviews_df_nomissing_unique['state'] = reviews_df_nomissing_unique['state'].map(state_mapping)

    # Format the Date into reviews using assumed date of January 1st, 2023
    reviews_df_nomissing_unique['review_date'] = reviews_df_nomissing_unique['review_time'].apply(parse_relative_date)
    print(reviews_df_nomissing_unique[['review_date', 'state']]) #Check Formatting

    # Create Year Columns
    reviews_df_nomissing_unique['review_year'] =  reviews_df_nomissing_unique['review_date'].dt.year

    # Format Rating columns
    reviews_df_nomissing_unique['review_rating'] = reviews_df_nomissing_unique['rating'].apply(parse_rating)
    print(reviews_df_nomissing_unique['review_rating']) #Check Formatting

    reviews_df_nomissing_unique.rename(columns={'review': 'review_text'}, inplace=True)
    #Drop other irrevelant columns
    print(reviews_df_nomissing_unique.info()) 
    # reviews_df_nomissing_unique.(drop)(columns=[['review_time', 'rating']], inplace=True)
    # print(reviews_df_nomissing_unique.info()) 

    # Preporcess texts
    reviews_df_nomissing_unique['review_text'] = reviews_df_nomissing_unique['review_text'].apply(preprocess_text)
    print (reviews_df_nomissing_unique ['review_text'])

    analyzer = SentimentIntensityAnalyzer()
    # apply get_sentiment function
    reviews_df_nomissing_unique[['sentiment_score', 'sentiment']] = reviews_df_nomissing_unique['review_text'].apply(get_sentiment)
    print("Sentiment")
    print(reviews_df_nomissing_unique)

    # Save Results to CSV File
    reviews_df_nomissing_unique.to_csv("McDonalds_Review_Sentiment_Analysis.csv")

except FileNotFoundError:
    print(f"Error: The file at {file_path} was not found.")
except pd.errors.EmptyDataError:
    print("Error: The file is empty.")
except pd.errors.ParserError:
    print("Error: There was a problem parsing the file.")
