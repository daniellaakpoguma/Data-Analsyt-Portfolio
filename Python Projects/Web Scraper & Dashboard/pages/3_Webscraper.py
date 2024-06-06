import streamlit as st

st.title("Web Scraper")

# datascraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_data(url):
    """
    Scrape data from a given URL and return a Pandas DataFrame.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            return pd.DataFrame(), f"Error fetching data: {response.status_code} - {response.text}"
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the review elements
        reviews = soup.find_all('li', class_='y-css-1jp2syp') 
        if not reviews:
            return pd.DataFrame(), "No reviews found on the page."
        
        # Initialize list to store review data
        reviews_data = []
        
        # Extract data from each review
        for review in reviews:
            review_data = {}
            
            # Extract reviewer's name and location
            reviewer_info_elem = review.find('div', class_='arrange-unit__09f24__rqHTg arrange-unit-fill__09f24__CUubG y-css-1iy1dwt')
            if reviewer_info_elem:
                reviewer_info = reviewer_info_elem.text.strip()
                reviewer_info_parts = reviewer_info.split('.')
                if len(reviewer_info_parts) >= 2:
                    reviewer_name = reviewer_info_parts[0].strip()
                    reviewer_location = reviewer_info_parts[1].strip()
                else:
                    reviewer_name = reviewer_info.strip()
                    reviewer_location = "Location Not Found"
            else:
                reviewer_name = "Reviewer Name Not Found"
                reviewer_location = "Location Not Found"
                
            # Extract review date
            review_date_elem = review.find('span', class_=' y-css-pw0opj')
            review_date = review_date_elem.text.strip() if review_date_elem else "Date Not Found"
                   
            # Extract Star Rating

            # Initialize review_rating with a default value
            review_rating = "Rating Not Found"

            # Find the span tag containing star icons
            star_elem = review.find('div', class_='y-css-9tnml4')

            # Check if the span tag exists
            if star_elem:
                # Find all the div elements within the span tag
                if star_elem.has_attr('aria_label'):
            
                    # Access the aria_label attribute
                    aria_label = star_elem['aria_label']
                
                    if '5 star rating' in aria_label:
                        review_rating = '5'
                    elif '4 star rating' in aria_label:
                        review_rating = '4'
                    elif '3 star rating' in aria_label:
                        review_rating = '3'
                    elif '2 star rating' in aria_label:
                        review_rating = '2'
                    else:
                        review_rating = '1'

            # Extract review text
            review_text_elem = review.find('p', class_='comment__09f24__D0cxf y-css-h9c2fl')
            review_text = review_text_elem.text.strip() if review_text_elem else "Review Text Not Found"
                
            # Store review data in a dictionary
            review_data = {
                'Reviewer Name': reviewer_name,
                'Reviewer Location': reviewer_location,
                'Review Date': review_date,
                'Review Rating': review_rating,
                'Review Text': review_text
            }
                
            # Append review data to the list
            reviews_data.append(review_data)

        return pd.DataFrame(reviews_data), None
    
    except requests.exceptions.RequestException as e:
        return pd.DataFrame(), f"Error: {e}"
    except Exception as e:
        return pd.DataFrame(), f"Error: {e}"


# Streamlit UI for URL input
url = st.text_input("Enter the URL of the page to scrape:")

if st.button("Scrape Data"):
    if url:
        data, error = scrape_data(url)
        if error:
            st.error(error)
        else:
            st.success(f"Successfully scraped {len(data)} reviews.")
            st.dataframe(data)
    else:
        st.error("Please enter a valid URL.")