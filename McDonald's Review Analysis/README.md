https://app.powerbi.com/groups/me/reports/bd549a01-0f8b-4c16-91e7-6afdfa38feb0/5fb49c8b17176a61a6c4?experience=power-bi


# McDonald's Review Analysis

## Table Of Contents

## I. Project Overview
This project is based off this [dataset](https://www.kaggle.com/datasets/nelgiriyewithana/mcdonalds-store-reviews), containing over 33,000 anonymized reviews of McDonald's stores in the United States, scraped from Google reviews. The dataset includes information such as store names, categories, addresses, geographic coordinates, review ratings, review texts, and timestamps. The project aims to evaluate customer sentiment based on the text gotten from the reviews. By analyzing textual data from customer reviews, this project seeks to uncover insights into customer opinions, identify trends in sentiment over time, and provide actionable recommendations to enhance customer satisfaction.

## II. Description of Approach
After the data was gotten from Kaggle, a new Python script was created
1.**Data Cleaning:**
- Missing values were looked for, and some were found in the Latitude column which was removed, alongside Longitude, Store Name and Category columns.
- Duplicates were removed
- White space were removed from all data cells

 
2. **Data Preparation:**
- Reviewer ID was set to the index of the data frame containing contents of the csv file
- Address was formatted into five seperate columns: Street Adress, City, State,  Zipcode, and Country
- State name columns were formatted to use their full names, instead of two letter words.
- Year column was also dervived form the Date column
- Review ratings were formatted only use the numerical values
- Column names were formatted to use the general format, and unnecessary columns were dropped
- Reviews with corrupt text (text with Non-ASCII characters) were removed
- Text was pre-processed by toeknixztaion and lemmetization

## III. Modeling
- SentimentIntensityAnalyzer was used to analyze sentiment of the text. A likert scale was used to get sentiment catgeoires between Strongly Positive, Posituve, Neutral, Negative, and Strongly Negtaive.
- Results were saved to a csv file

## IV. Visualization


## References 
1. https://www.kaggle.com/datasets/nelgiriyewithana/mcdonalds-store-reviews 
