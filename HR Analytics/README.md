# HR Attrition Analysis
This project aims to calculate the rate at which employees leave an organisation and identify the possible underlying reasons for their departure.

## General Understanding
This project uses a fictitious dataset downloaded from Kaggle (https://www.kaggle.com/datasets/rishikeshkonapure/hr-analytics-prediction). 

## Attrition Analysis
### Employee Attrition at an general company level
```sql
SELECT Attrition, COUNT(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition;
```
