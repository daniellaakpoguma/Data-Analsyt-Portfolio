import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os
import tempfile

# Function to scrape Instagram
def instagram_scraper(username, password, search_term):
    PATH = r"/usr/local/bin/chromedriver"
    if not os.path.exists(PATH):
        st.error("Chromedriver path is incorrect or chromedriver.exe does not exist.")
        return []

    driver = webdriver.Chrome(PATH)

    driver.get("https://www.instagram.com/")

    # Login
    time.sleep(5)
    username_input = driver.find_element_by_css_selector("input[name='username']")
    password_input = driver.find_element_by_css_selector("input[name='password']")
    username_input.clear()
    password_input.clear()
    username_input.send_keys(username)
    password_input.send_keys(password)
    login = driver.find_element_by_css_selector("button[type='submit']").click()

    # Save login info? and Turn on notifications
    time.sleep(10)
    notnow = driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
    time.sleep(10)
    notnow2 = driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()

    # Search
    time.sleep(5)
    searchbox = driver.find_element_by_css_selector("input[placeholder='Search']")
    searchbox.clear()
    searchbox.send_keys(search_term)
    time.sleep(5)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(5)
    searchbox.send_keys(Keys.ENTER)

    # Scroll and collect posts
    scrolldown = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    match=False
    while(match==False):
        last_count = scrolldown
        time.sleep(3)
        scrolldown = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        if last_count==scrolldown:
            match=True

    # Collect post links
    posts = []
    links = driver.find_elements_by_tag_name('a')
    for link in links:
        post = link.get_attribute('href')
        if '/p/' in post:
            posts.append(post)

    # Download images and videos
    downloaded_files = []
    for post in posts:
        driver.get(post)
        shortcode = driver.current_url.split("/")[-2]
        time.sleep(7)
        if driver.find_elements_by_css_selector("img[style='object-fit: cover;']"):
            download_url = driver.find_element_by_css_selector("img[style='object-fit: cover;']").get_attribute('src')
            file_path = f"{shortcode}.jpg"
            urllib.request.urlretrieve(download_url, file_path)
            downloaded_files.append(file_path)
        elif driver.find_elements_by_css_selector("video[type='video/mp4']"):
            download_url = driver.find_element_by_css_selector("video[type='video/mp4']").get_attribute('src')
            file_path = f"{shortcode}.mp4"
            urllib.request.urlretrieve(download_url, file_path)
            downloaded_files.append(file_path)
        time.sleep(5)

    driver.quit()
    return downloaded_files

# Streamlit App
st.title('Instagram Scraper')

username = st.text_input('Instagram Username')
password = st.text_input('Instagram Password', type='password')
search_term = st.text_input('Search Term')

if st.button('Scrape'):
    if username and password and search_term:
        with st.spinner('Scraping...'):
            try:
                downloaded_files = instagram_scraper(username, password, search_term)
                st.success('Scraping completed!')
                for file in downloaded_files:
                    st.write(file)
                    if file.endswith('.jpg'):
                        st.image(file)
                    elif file.endswith('.mp4'):
                        st.video(file)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error('Please provide all inputs')
