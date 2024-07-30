import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.title("Poshmark Insights")
keyword_input = st.text_input("Enter keyword:")

if st.button("Scrape"):
    if keyword_input:
        # URL with user input
        base_url = 'https://poshmark.ca/search?query='
        query_input = keyword_input.replace(' ', '%20')  # Replace spaces with URL encoding
        url = f"{base_url}{query_input}&type=listings&src=dir"

        # Headers for request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        # Make the HTTP request
        response = requests.get(url, headers=headers)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # List to hold the item data
        items_data = []

        # Iterate over each item card in the soup
        for item in soup.find_all('div', class_='card'):
            # Find the item name and price within the current item card
            item_name = item.find('a', class_='tile__title').get_text() if item.find('a', class_='tile__title') else 'N/A'
            item_price = item.find('span', class_='p--t--1').get_text() if item.find('span', class_='p--t--1') else 'N/A'
            item_size = item.find('a', class_='tile__details__pipe__size ellipses').get_text() if item.find('a', class_='tile__details__pipe__size ellipses') else 'N/A'
            item_brand = item.find('a', class_='tile__details__pipe__brand ellipses router-link-exact-active router-link-active').get_text() if item.find('a', class_='tile__details__pipe__brand ellipses router-link-exact-active router-link-active') else 'N/A'

            # Get the absolute URL
            poshmark_link = 'https://poshmark.ca'
            link = item.find('a', class_='tile__covershot').get('href') if item.find('a', class_='tile__covershot') else 'N/A'
            item_link = poshmark_link + link

            # Append the item data to the list
            items_data.append({
                'Brand': item_brand,
                'Item Name': item_name,
                'Price': item_price,
                'Size': item_size,
                'Product Link': item_link
            })

        # Create a DataFrame from the list of items
        items_df = pd.DataFrame(items_data)

        # Display the DataFrame in Streamlit
        st.write(items_df)

    else:
        st.write('Please enter a query.')
