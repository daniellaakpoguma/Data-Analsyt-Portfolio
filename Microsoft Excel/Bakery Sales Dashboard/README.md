# Bakery Sales Analysis
## Project Overview
# Dataset Description:
This analysis utilizes basket data collected from a small bakery in Korea (https://www.kaggle.com/datasets/hosubjeong/bakery-sales/code). The primary objective is to understand the relationship between sales patterns, specific days of the week, and times of day.

# Goals:
- Identify correlations between sales and specific time periods.
- Analyze how different times of the day affect sales.
- Explore key performance indicators (KPIs) to gauge business performance and inform decision-making.

# Methodology
After visualizing the sales data in Microsoft Excel, advanced market basket analysis and association rules will be conducted using R in RStudio. This step aims to uncover deeper insights into customer purchasing behavior and identify potential opportunities for business improvement.

## Data Preparation
- Checked for duplciates, none found
- Removed 'Place' Column as information in the column is not needed, and majority of the data in teh coumn is null
- Delted last few rows, where it seems that the bakery stopped taking orders due to covid
- Replaced day of week values with corect values
- fIXED inconssitemnscies in prcie dashboard
  
## Data Visualization
![final_dashboard](https://github.com/user-attachments/assets/0cba4077-8466-4575-afcf-bdd6b4f4ea82)

## Association Rule Mining
- Binary conversion in RStudio for Association Rules
- copy and paste the rules

