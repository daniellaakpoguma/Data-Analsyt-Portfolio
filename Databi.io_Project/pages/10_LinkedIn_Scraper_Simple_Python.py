import time
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import warnings
warnings.filterwarnings('ignore')


class LinkedInScraper:

    @staticmethod
    def webdriver_setup():
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Set the path to chromedriver
        driver_path = '/usr/local/bin/chromedriver'
        
        # Create a service object
        service = Service(driver_path)
        
        # Initialize the webdriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        
        return driver

    @staticmethod
    def build_url(keywords, job_location):
        b = ['%20'.join(i.split()) for i in keywords]
        keyword = '%2C%20'.join(b)
        link = f"https://www.linkedin.com/jobs/search?keywords={keyword}&location={job_location}&locationId=&geoId=103644278&f_TPR=r604800&position=1&pageNum=0"
        return link

    @staticmethod
    def open_link(driver, link):
        while True:
            try:
                driver.get(link)
                timeout_value = 10
                driver.implicitly_wait(timeout_value)
                time.sleep(3)
                driver.find_element(by=By.CSS_SELECTOR, value='span.switcher-tabs__placeholder-text.m-auto')
                return
            except TimeoutException as te:
                print(f"Timeout waiting for page to load: {te}")
            except NoSuchElementException:
                continue

    @staticmethod
    def link_open_scrolldown(driver, link, job_count):
        LinkedInScraper.open_link(driver, link)
        for i in range(job_count):
            body = driver.find_element(by=By.TAG_NAME, value='body')
            body.send_keys(Keys.PAGE_UP)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(2)
            try:
                driver.find_element(by=By.CSS_SELECTOR, value="button[aria-label='See more jobs']").click()
                driver.implicitly_wait(5)
            except:
                pass

    @staticmethod
    def job_title_filter(scrap_job_title, user_job_title_input):
        user_input = [i.lower().strip() for i in user_job_title_input]
        scrap_title = [i.lower().strip() for i in [scrap_job_title]]
        confirmation_count = sum(all(j in scrap_title[0] for j in i.split()) for i in user_input)
        return scrap_job_title if confirmation_count > 0 else np.nan

    @staticmethod
    def scrap_company_data(driver, job_title_input, job_location):
        company_name = [i.text for i in driver.find_elements(by=By.CSS_SELECTOR, value='h4[class="base-search-card__subtitle"]')]
        company_location = [i.text for i in driver.find_elements(by=By.CSS_SELECTOR, value='span[class="job-search-card__location"]')]
        job_title = [i.text for i in driver.find_elements(by=By.CSS_SELECTOR, value='h3[class="base-search-card__title"]')]
        website_url = [i.get_attribute('href') for i in driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')]

        df = pd.DataFrame({'Company Name': company_name, 'Job Title': job_title, 'Location': company_location, 'Website URL': website_url})
        df['Job Title'] = df['Job Title'].apply(lambda x: LinkedInScraper.job_title_filter(x, job_title_input))
        df['Location'] = df['Location'].apply(lambda x: x if job_location.lower() in x.lower() else np.nan)
        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    @staticmethod
    def scrap_job_description(driver, df, job_count):
        website_url = df['Website URL'].tolist()
        job_description = []
        description_count = 0
        for url in website_url:
            try:
                LinkedInScraper.open_link(driver, url)
                driver.find_element(by=By.CSS_SELECTOR, value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]').click()
                driver.implicitly_wait(5)
                time.sleep(1)
                data = driver.find_elements(by=By.CSS_SELECTOR, value='div[class="show-more-less-html__markup relative overflow-hidden"]')[0].text
                if data.strip():
                    job_description.append(data)
                    description_count += 1
                else:
                    job_description.append('Description Not Available')
            except:
                job_description.append('Description Not Available')
            if description_count == job_count:
                break
        df = df.iloc[:len(job_description), :]
        df['Job Description'] = job_description
        df = df[df['Job Description'] != 'Description Not Available'].dropna()
        df.reset_index(drop=True, inplace=True)
        return df

    @staticmethod
    def main(keywords, job_location, job_count):
        driver = LinkedInScraper.webdriver_setup()
        link = LinkedInScraper.build_url(keywords, job_location)
        LinkedInScraper.link_open_scrolldown(driver, link, job_count)
        df = LinkedInScraper.scrap_company_data(driver, keywords, job_location)
        df_final = LinkedInScraper.scrap_job_description(driver, df, job_count)
        driver.quit()
        print(df_final)


if __name__ == "__main__":
    keywords = ["Software Engineer"]
    job_location = "North America"
    job_count = 10
    LinkedInScraper.main(keywords, job_location, job_count)
