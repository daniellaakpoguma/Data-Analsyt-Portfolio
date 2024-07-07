import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

class LinkedInScraperTest:

    @staticmethod
    def webdriver_setup():
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Set the path to chromedriver
        driver_path = '/usr/local/bin/chromedriver'
        service = ChromeService(executable_path=driver_path)
        
        # Initialize the webdriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        
        return driver

    def get_userinput(self):
        # Placeholder for user input
        keyword_input = ['Data Scientist']
        job_location = 'North America'
        job_count = 5
        submit = True
        
        return keyword_input, job_location, job_count, submit

    def build_url(self, keyword, job_location):
        b = []
        for i in keyword:
            x = i.split()
            y = '%20'.join(x)
            b.append(y)

        keyword = '%2C%20'.join(b)
        link = f"https://www.linkedin.com/jobs/search?keywords={keyword}&location={job_location}&locationId=&geoId=103644278&f_TPR=r604800&position=1&pageNum=0"

        return link

    def open_link(self, driver, link):
        while True:
            # Break the Loop if the Element is Found, Indicating the Page Loaded Correctly
            try:
                driver.get(link)
                timeout_value = 10  # Example: set the timeout to 10 seconds
                driver.implicitly_wait(timeout_value)
                time.sleep(3)
                driver.find_element(by=By.CSS_SELECTOR, value='span.switcher-tabs__placeholder-text.m-auto')
                return
            
            # Retry Loading the Page
            except TimeoutException as te:
                st.error(f"Timeout waiting for page to load: {te}")
            except NoSuchElementException:
                continue

    def link_open_scrolldown(self, driver, link, job_count):
        # Open the Link in LinkedIn
        self.open_link(driver, link)

        # Scroll Down the Page
        for i in range(0,job_count):
            # Simulate clicking the Page Up button
            body = driver.find_element(by=By.TAG_NAME, value='body')
            body.send_keys(Keys.PAGE_UP)
            # Scoll down the Page to End
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(2)
            # Click on See More Jobs Button if Present
            try:
                x = driver.find_element(by=By.CSS_SELECTOR, value="button[aria-label='See more jobs']").click()
                driver.implicitly_wait(5)
            except:
                pass

    def run_test(self):
        driver = self.webdriver_setup()
        keyword_input, job_location, job_count, submit = self.get_userinput()
        if submit:
            if keyword_input and job_location:
                try:
                    link = self.build_url(keyword_input, job_location)
                    self.link_open_scrolldown(driver, link, job_count)
                    st.write("Test Passed: Job listings loaded successfully.")
                except Exception as e:
                    st.write(f"Test Failed: {e}")
                finally:
                    driver.quit()
            else:
                st.write("Test Failed: Keyword input or job location is empty.")
        else:
            st.write("Test Failed: Submit flag is False.")

if __name__ == "__main__":
    scraper_test = LinkedInScraperTest()
    scraper_test.run_test()
