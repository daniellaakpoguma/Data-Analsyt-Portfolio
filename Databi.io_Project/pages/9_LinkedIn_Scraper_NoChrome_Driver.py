import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def build_url(keywords, job_location):
    b = ['%20'.join(i.split()) for i in keywords]
    keyword = '%2C%20'.join(b)
    link = f"https://www.linkedin.com/jobs/search?keywords={keyword}&location={job_location}"
    return link

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
            'title': title,
            'company': company.text.strip().replace('\n', ' ') if company else '',
            'location': location.text.strip() if location else '',
            'date': date,
            'job_url': job_url,
        }
        joblist.append(job)

    df = pd.DataFrame(joblist)
    return df.head(job_count)

def main():
    st.title("LinkedIn Job Scraper")

    with st.form(key='linkedin_scarp'):
        st.header("Search Parameters")
        keyword_input = st.text_input(label='Keyword (comma-separated)').split(',')
        job_location = st.text_input(label='Job Location', value='North America')
        job_count = st.number_input(label='Job Count', min_value=1, value=10, step=1)
        submit = st.form_submit_button(label='Submit')

    if submit and keyword_input and job_location:
        url = build_url(keyword_input, job_location)
        df = scrape_job_listings(url, job_count)

        if not df.empty:
            st.header("Job Listings")
            st.write(df)

            st.header("Job Details")
            for idx, row in df.iterrows():
                st.markdown(f"[{row['title']} at {row['company']}]({row['job_url']})", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
