# Second Hand Shopping Insights
## Project Overview
This project aims to understand Poshmark data by analyzing insights into different categories, price ranges, and the services offered. The goal is to gain a comprehensive understanding of the platform’s product offerings, pricing trends, and seller performance. By examining these aspects, I aim to uncover patterns and trends that will provide a deeper understanding of Poshmark’s marketplace. 

## Description of Approach
1. Information scrapped from Poshamrk website Selenuim Web driver, BeautifulSoup
2. Created Streamlit application to be used for other users to get information from Poshmark themselves using keyword input
3. CSV files were gotten for top 10 categories gotten from this list: https://poshwatch.io/top-categories-on-poshmark

## Database
- The CSV were imported into various tables in the database

## SQL 
- CSV files downloaded into SQL as flat file

## Power BI
- 'N/A' values were moved in Colors column in all tables
- Replaced 'N/A' in brand name with 'Unknwon'
- Capitalized each word in Brand name
- Clean and Trimmed text

## Next Steps:
1. Data downloaded into SQL, so ELT process can be done.
2. SQL can be used to transform data
3. Explore data using SQL and so on
4. Visualization done in Tableau

5. Image Classification to be done on images 
