import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

def depop_query(keyword_input):
    st.header("Depop Insights")
    
    # Base URL for Depop search
    base_url = 'https://www.depop.com/search/?q='
    query_input = keyword_input.replace(' ', '+')  # Replace spaces with '+'
    url = f"{base_url}{query_input}"

    st.write(f"Requesting URL: {url}")

    # Headers for request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.depop.com/',
    }

    # Make the HTTP request
    response = requests.get(url, headers=headers)
    st.write(f"HTTP Status Code: {response.status_code}")

    # Check if request was successful
    if response.status_code == 200:
        st.write("Request successful!")
    else:
        st.write("Request failed.")
        return

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Print raw HTML for debugging
    st.write("Raw HTML:")
    st.write(soup.prettify())

    # List to hold the item data
    items_data = []

    # Iterate over each item card in the soup
    for item in soup.find_all('div', class_='styles__StyledAttributesContainer-sc-e33cc28-11 cBjQyU'):
        st.write("Item HTML:")
        st.write(item)
        
        # Extract and debug item details
        item_brand_tag = item.find('p', class_='sc-eDnWTT styles__StyledBrandNameText-sc-e33cc28-21 kcKICQ kOTKTw')
        item_brand = item_brand_tag.get_text(strip=True) if item_brand_tag else 'N/A'
        st.write(f"Extracted Brand: {item_brand}")
        
        item_price_tag = item.find('p', class_='sc-eDnWTT Price-styles__FullPrice-sc-f7c1dfcc-0 fRxqiS hmFDou')
        item_price = item_price_tag.get_text(strip=True) if item_price_tag else 'N/A'
        st.write(f"Extracted Price: {item_price}")
        
        item_size_tag = item.find('p', class_='sc-eDnWTT styles__StyledSizeText-sc-e33cc28-12 kcKICQ BpbxN')
        item_size = item_size_tag.get_text(strip=True) if item_size_tag else 'N/A'
        st.write(f"Extracted Size: {item_size}")

        # Append the item data to the list
        items_data.append({
            'Brand': item_brand,
            'Price': item_price,
            'Size': item_size,
        })

    # Create a DataFrame from the list of items
    items_df = pd.DataFrame(items_data)

    # Display the DataFrame in Streamlit
    st.write("Items DataFrame:")
    st.write(items_df)
