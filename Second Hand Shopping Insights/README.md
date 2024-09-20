
# Second Hand Shopping Insights

## Project Overview
This project focuses on extracting, transforming, and analyzing data from the Poshmark marketplace. By understanding product categories, pricing trends, and seller performance, the aim is to uncover valuable insights from second-hand shopping data. The process spans web scraping, data transformation, and visualization, leveraging tools such as Python (Selenium, BeautifulSoup), SQL, and Streamlit.

## Description of Approach
1. **Web Scraping**: 
   - Scraped Poshmark data using Selenium WebDriver and BeautifulSoup for the top 10 product categories (source: https://poshwatch.io/top-categories-on-poshmark).
   - The data includes product details such as brand, item name, price, size, description, and more.
   
2. **Streamlit Application**: 
   - Developed an interactive app allowing users to scrape Poshmark using custom keywords.

3. **Data Cleaning**:
   - Performed data cleaning in Python, including cleaning and trimming text.

## Database
- Imported CSV files into a relational SQL database.
- Organized data into separate tables for each category (shoes, tops, etc.).

## SQL 
- Imported data as flat files and set up relational tables.
- Performed initial cleaning and transformation using SQL queries.


## Next Steps
- Develop an image classification model to categorize product images.
