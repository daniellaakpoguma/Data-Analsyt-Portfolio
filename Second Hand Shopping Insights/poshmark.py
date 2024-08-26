import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def poshmark_query(keyword_input, brand='', color='', size='', min_price=0, max_price=1000, target_count=100, scroll_pause_time=2):
    st.header("Poshmark Insights")

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Build the URL with filters
    base_url = f'https://poshmark.ca/search?query={keyword_input.replace(" ", "%20")}'
    if brand:
        base_url += f'&brand={brand}'
    if color:
        base_url += f'&color={color}'
    if size:
        base_url += f'&size={size}'
    if min_price or max_price:
        base_url += f'&priceMin={min_price}&priceMax={max_price}'

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

            items_data.append({
                'Brand': item_brand,
                'Item Name': item_name,
                'Price': item_price,
                'Size': item_size,
                'Product Link': item_link
            })

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    driver.quit()

    items_df = pd.DataFrame(items_data)
    st.write(items_df)

