import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def poshmark_query(keyword_input):
    st.header("Poshmark Insights")
    target_count=5
    scroll_pause_time=2
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Build the URL with filters
    base_url = f'https://poshmark.ca/search?query={keyword_input.replace(" ", "%20")}'

    driver.get(base_url)

    items_data = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(items_data) < target_count:
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for item in soup.find_all('div', class_='card'):
            if len(items_data) >= target_count:
                break
            
            item_name = item.find('a', class_='tile__title').get_text() if item.find('a', class_='tile__title') else 'N/A'
            item_price = item.find('span', class_='p--t--1').get_text() if item.find('span', class_='p--t--1') else 'N/A'
            item_size = item.find('a', class_='tile__details__pipe__size ellipses').get_text().replace('Size: ', '') if item.find('a', class_='tile__details__pipe__size ellipses') else 'N/A'
            item_brand = item.find('a', class_='tile__details__pipe__brand ellipses').get_text(strip=True) if item.find('a', class_='tile__details__pipe__brand ellipses') else 'N/A'

            poshmark_link = 'https://poshmark.ca'
            link = item.find('a', class_='tile__covershot').get('href') if item.find('a', class_='tile__covershot') else 'N/A'
            item_link = poshmark_link + link


            # Navigate to the product page to scrape more details
            if item_link != 'N/A':
                driver.get(item_link)
                time.sleep(2)  # Let the page load
                
                product_soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Scrape additional details from the product page
                description = product_soup.find('div', class_='listing__description').get_text() if product_soup.find('div', class_='listing__description') else 'N/A'
                extra_info_div = product_soup.find('div', class_='p--t--3')

                # Initialize a variable to store extra info
                extra_info = []

                # If the div exists, find the list items (li) inside and extract the text
                if extra_info_div:
                    for li in extra_info_div.find_all('li', class_='listing__disclaimer__item'):
                        # Extract the text inside the <p> tag
                        info = li.find('p', class_='listing__disclaimer__message').get_text(strip=True)
                        extra_info.append(info)

                # If extra_info contains data, join it into a string; otherwise, set it as 'N/A'
                extra_info = ', '.join(extra_info) if extra_info else 'N/A'

                # Initialize an empty list for colors
                colors = []

                # Find all color-related divs
                color_buttons = product_soup.find_all('div', class_='btn btn--tag tag-details__btn')

                # Extract color names
                for color_item in color_buttons:
                    color_name = color_item['data-et-prop-listing_color'] if color_item.has_attr('data-et-prop-listing_color') else 'N/A'
                    # Append the color name to the list
                    colors.append(color_name)

                # If colors are found, join them into a single string
                colors_string = ', '.join(colors) if colors else 'N/A'

                # Initialize variables to store extracted data
                listings = 'N/A'
                sold_listings = 'N/A'
                avg_ship_time = 'N/A'
                love_notes = 'N/A'

                # Find the seller details container
                seller_details_div = product_soup.find('div', class_='seller-details__stats')

                # Extract information from each relevant div
                if seller_details_div:
                    for item in seller_details_div.find_all('div', class_='tc--g'):
                        # Extract the h4 tag's text which contains the numeric values
                        h4_tag = item.find('h4')
                        numeric_value = h4_tag.get_text(strip=True) if h4_tag else 'N/A'
                        
                        # Determine which statistic the text belongs to
                        if 'Sold Listings' in item.get_text():
                            sold_listings = numeric_value
                        elif 'Listings' in item.get_text():
                            listings = numeric_value
                        elif 'Avg. Ship time' in item.get_text():
                            avg_ship_time = numeric_value
                        elif 'Love Notes' in item.get_text():
                            love_notes = numeric_value

                 # Store all data into the dictionary
                items_data.append({
                    'Brand': item_brand,
                    'Item Name': item_name,
                    'Price': item_price,
                    'Size': item_size,
                    'Product Link': item_link,
                    'Description':  description,
                    'Extra Info': extra_info,
                    'Colors':  colors_string, 
                    'No Of Seller Listings': listings, 
                    'No Of Sold Seller Listings': sold_listings,
                    'Seller Avg. Shipping Time': avg_ship_time,
                    'No of Seller Love Notes': love_notes,
                })
             # Return to the main search results
            driver.back()
            time.sleep(1)
            
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    driver.quit()

    items_df = pd.DataFrame(items_data)
    st.write(items_df)

