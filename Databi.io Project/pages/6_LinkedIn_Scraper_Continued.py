import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def build_job_url(keywords, job_location):
    b = ['%20'.join(i.split()) for i in keywords]
    keyword = '%2C%20'.join(b)
    link = f"https://www.linkedin.com/jobs/search?keywords={keyword}&location={job_location}"
    return link

def build_linkedin_url(search_type, keywords):
    base_url = "https://www.linkedin.com/search/results/"
    params = {
        "keywords": keywords,
        "origin": "SWITCH_SEARCH_VERTICAL",
        "searchType": search_type
    }
    return base_url + "?" + "&".join([f"{key}={value}" for key, value in params.items()])

def scrape_job_listings(url, job_count):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    joblist = []
    try:
        divs = soup.find_all('div', class_='base-search-card__info')
    except:
        print("Empty page, no jobs found")
        return pd.DataFrame()

    for item in divs:
        title = item.find('h3').text.strip()
        company = item.find('a', class_='hidden-nested-link')
        location = item.find('span', class_='job-search-card__location')
        parent_div = item.parent
        entity_urn = parent_div['data-entity-urn']
        job_posting_id = entity_urn.split(':')[-1]
        job_url = 'https://www.linkedin.com/jobs/view/' + job_posting_id + '/'

        date_tag_new = item.find('time', class_='job-search-card__listdate--new')
        date_tag = item.find('time', class_='job-search-card__listdate')
        date = date_tag['datetime'] if date_tag else (date_tag_new['datetime'] if date_tag_new else '')

        job = {
            'Title': title,
            'Company': company.text.strip().replace('\n', ' ') if company else '',
            'Location': location.text.strip() if location else '',
            'Date': date,
            'Job URL': job_url,
        }
        joblist.append(job)

    df = pd.DataFrame(joblist)
    return df.head(job_count)

def scrape_linkedin_search_results(url, result_count):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = []
    try:
        items = soup.find_all('li', class_='search-result')
    except:
        print("Empty page, no results found")
        return pd.DataFrame()

    for item in items[:result_count]:
        # Parse individual result item
        title = item.find('span', class_='name actor-name').text.strip()
        subtitle = item.find('p', class_='subline-level-1').text.strip()
        link = item.find('a')['href'] if item.find('a') else ''
        description = item.find('p', class_='subline-level-2').text.strip()

        result = {
            'Title': title,
            'Subtitle': subtitle,
            'Link': link,
            'Description': description
        }
        results.append(result)

    df = pd.DataFrame(results)
    return df.head(result_count)

def main():
    st.title("Linkedin Research Data - Part 2")

    with st.form(key='linkedin_search_form'):
        st.header("Search Parameters")
        keyword_input = st.text_input(label='Enter Keywords (comma-separated)').split(',')
        location = st.text_input(label='Location', value='North America')
        search_type = st.selectbox(label='Search Type', options=['jobs', 'people', 'companies', 'posts'])
        result_count = st.number_input(label='Result Count', min_value=1, value=10, step=1)
        submit = st.form_submit_button(label='Search')

    if submit and keyword_input and location and search_type == 'jobs':
        url = build_job_url(keyword_input, location)
        df = scrape_job_listings(url, result_count)

        if not df.empty:
            st.header(f"{search_type.capitalize()} Search Results")
            st.table(df)

    elif submit and keyword_input and search_type in ['people', 'companies', 'posts']:
        url = build_linkedin_url(search_type, keyword_input)
        df = scrape_linkedin_search_results(url, result_count)

        if not df.empty:
            st.header(f"{search_type.capitalize()} Search Results")
            st.table(df)

if __name__ == "__main__":
    main()
