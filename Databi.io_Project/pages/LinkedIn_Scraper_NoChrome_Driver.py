import time
import numpy as np
import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup
from streamlit_extras.add_vertical_space import add_vertical_space


def build_url(keywords, job_location):
    b = ['%20'.join(i.split()) for i in keywords]
    keyword = '%2C%20'.join(b)
    link = f"https://www.linkedin.com/jobs/search?keywords={keyword}&location={job_location}&locationId=&geoId=103644278&f_TPR=r604800&position=1&pageNum=0"
    return link


def scrape_job_listings(url, job_count):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    job_titles = [job.text for job in soup.find_all('h3', class_='base-search-card__title')]
    company_names = [company.text for company in soup.find_all('h4', class_='base-search-card__subtitle')]
    locations = [location.text for location in soup.find_all('span', class_='job-search-card__location')]
    job_links = [link['href'] for link in soup.find_all('a', {'data-tracking-control-name': 'public_jobs_jobs-search-card_click'})]

    df = pd.DataFrame({
        'Job Title': job_titles[:job_count],
        'Company Name': company_names[:job_count],
        'Location': locations[:job_count],
        'Job Link': job_links[:job_count]
    })
    return df


def main():
    st.title("LinkedIn Job Scraper (Without ChromeDriver)")

    with st.form(key='linkedin_scarp'):
        add_vertical_space(1)
        col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap='medium')
        with col1:
            keyword_input = st.text_input(label='Keyword').split(',')
        with col2:
            job_location = st.text_input(label='Job Location', value='North America')
        with col3:
            job_count = st.number_input(label='Job Count', min_value=1, value=1, step=1)
        submit = st.form_submit_button(label='Submit')
        add_vertical_space(1)

    if submit and keyword_input and job_location:
        url = build_url(keyword_input, job_location)
        df = scrape_job_listings(url, job_count)
        st.write(df)


if __name__ == "__main__":
    main()
