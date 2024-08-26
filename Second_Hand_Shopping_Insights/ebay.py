import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

def ebay_query(keyword_input):
    st.header("Ebay Insights")
    # Updated base URL for eBay search
    base_url = 'https://www.ebay.ca/sch/i.html?_nkw='
    query_input = keyword_input.replace(' ', '+')  # Replace spaces with '+' as commonly used in URLs
    url = f"{base_url}{query_input}&_sacat=0"

    
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
    for item in soup.find_all('div', class_='s-item__info clearfix'):
        # Find the item name and price within the current item card
        item_name = item.find('div', class_='s-item__title').get_text() if item.find('div', class_='s-item__title') else 'N/A'
        if item_name == 'Shop on eBay':
            continue  # Skip this item and move to the next one
        item_price = item.find('span', class_='ITALIC').get_text() if item.find('span', class_='ITALIC') else 'N/A'
        # item_size = item.find('a', class_='tile__details__pipe__size ellipses').get_text() if item.find('a', class_='tile__details__pipe__size ellipses') else 'N/A'
        # item_brand = item.find('a', class_='tile__details__pipe__brand ellipses').get_text(strip=True) if item.find('a', class_='tile__details__pipe__brand ellipses') else 'N/A'

        # Append the item data to the list
        items_data.append({
            #'Brand': item_brand,
            'Item Name': item_name,
            'Price': item_price,
            #'Size': item_size,
            #'Product Link': item_link
        })

        
    # Create a DataFrame from the list of items
    items_df = pd.DataFrame(items_data)

    # Display the DataFrame in Streamlit
    st.write(items_df)

        
