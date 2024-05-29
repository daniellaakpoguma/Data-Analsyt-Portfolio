import streamlit as st
from datascraper import scrape_data

def show_scraper():
    st.title("Web Scraper")

    # Get user input
    url = st.text_input("Enter the URL to scrape:")

    # Scrape data and display the results
    if st.button("Scrape Data"):
        df, error_message = scrape_data(url)
        if error_message:
            st.error(error_message)
        else:
            if not df.empty:
                st.write(df)
            else:
                st.write("No data found.")
