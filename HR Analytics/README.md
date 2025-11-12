# HR Attrition Analysis
Employee turnover is a major cost for organisations. Understanding which employees are at higher risk of leaving allows HR to implement targeted retention strategies. This project aims to do just that by calculating the rate at which employees leave an organisation and identifying the possible underlying reasons for their departure.

![Cover Image](Attrition%20Analysis/images/cover_image.png)

## Data Description
- Source: Kaggle (https://www.kaggle.com/datasets/rishikeshkonapure/hr-analytics-prediction)
<table>
  <tr>
    <td>
	  - EmployeeNumber <br>
      - Age <br>
      - Attrition <br>
      - BusinessTravel <br>
      - DailyRate <br>
      - Department <br>
      - DistanceFromHome <br>
      - Education <br>
      - EducationField <br>
      - EmployeeCount <br>
      - EnvironmentSatisfaction
    </td>
    <td>
      - Gender <br>
      - HourlyRate <br>
      - JobInvolvement <br>
      - JobLevel <br>
      - JobRole <br>
      - JobSatisfaction <br>
      - MaritalStatus <br>
      - MonthlyIncome <br>
      - MonthlyRate <br>
      - NumCompaniesWorked <br>
      - Over18
    </td>
    <td>
      - OverTime <br>
      - PercentSalaryHike <br>
      - PerformanceRating <br>
      - RelationshipSatisfaction <br>
      - StandardHours <br>
      - StockOptionLevel <br>
      - TotalWorkingYears <br>
      - TrainingTimesLastYear <br>
      - WorkLifeBalance <br>
      - YearsAtCompany <br>
      - YearsInCurrentRole <br>
      - YearsSinceLastPromotion <br>
      - YearsWithCurrManager
    </td>
  </tr>
</table>
- The CSV file was imported into MySQL Workbench in the 'hr_schema'

## Methods
- Data Cleaning:
  	- Renaming columns: The 'Age' column was renamed to remove the character that was put during the import process.
	 ```sql
  	# Renaming Columns
	ALTER TABLE hr_employee_attrition
  	RENAME COLUMN `ï»¿Age` to `Age`;
	 ```
  	- Removing Duplicates: Duplicate rows were removed, based on 'EmployeeNumber'. No duplicates were found.
  	```sql
	SELECT EmployeeNumber
	FROM hr_employee_attrition
	GROUP BY EmployeeNumber
	HAVING COUNT(*) > 1;
   	```
   - Deleting Redundant Columns: 'StandardHours' column was removed because every employee works 80 hours. 'Over18' column was removed because all employees are above 18. 'PerformanceRating' is also fairly constant with values being either 3 or 4, but I'm choosing to keep it.
	 ```sql
     # Deleting Redundant Columns
	 ALTER TABLE hr_employee_attrition
	 DROP COLUMN StandardHours;

  	 ALTER TABLE hr_employee_attrition
	 DROP COLUMN Over18;
	
	 ALTER TABLE hr_employee_attrition
	 DROP COLUMN EmployeeCount;
	 ```
(TO BE MADE BETTER LATER)
- Data Analysis:
  - We aim to uncover patterns in attrition by single-variable analysis and double-variable analysis
---

## General Data Understanding
Before we proceed, we want to gain a high-level understanding of the dataset by examining key metrics within this company's database. This step helps establish context and highlights any potential patterns or issues early on.
- Total Number of Employees: 1470
![Employee Number](Attrition%20Analysis/images/general_employee_count.png)
```sql
SELECT COUNT(*) AS no_of_employees
FROM hr_employee_attrition;
```
- Attrition Rate Overall: 16.12%
![General Attrition](Attrition%20Analysis/images/general_employee_count.png)
```sql
SELECT (CAST(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100 AS attrition_rate
FROM hr_employee_attrition;
```
- Min, Max and Avg Age of Employees:
![ages](Attrition%20Analysis/images/min-max-avg-age.png)
```sql
SELECT MIN(Age), MAX(Age), AVG(Age)
FROM hr_employee_attrition;
```
- Gender distribution: 882 Male, 588 Female
![Gender Distribution](Attrition%20Analysis/images/employees_by_gender.png)
```sql
# No of employees by gender 
SELECT Gender, COUNT(*) AS no_of_employees
FROM hr_employee_attrition
GROUP BY Gender;
```
- Average years at company: 7 years
```sql
SELECT AVG(YearsAtCompany)  AS average_years_at_working
FROM hr_employee_attrition;
```
- Average monthly income: $6,500
```sql
SELECT AVG(MonthlyIncome) AS avg_monthly_income
FROM  hr_employee_attrition
```
- Most common job role: Sales Executive
![Common_Job_Role](Attrition%20Analysis/images/\most_common_job_role.png)
```sql
SELECT JobRole, COUNT(*)
FROM  hr_employee_attrition
GROUP BY JobRole;
```
- Most common education field: Life Sciences
![Education Field Distribution](Attrition%20Analysis/images/no_of_employees_education_field.png)
```sql
SELECT EducationField, COUNT(*) AS no_of_employees
FROM hr_employee_attrition
GROUP BY EducationField;
```

## Attrition Analysis
In this section, we dive deeper into the dataset by examining individual variables that may influence employee attrition. By analysing one variable at a time, we aim to identify patterns and potential risk factors that could contribute to an employee’s decision to leave the company.

### Personal Info
#### Employee Attrition by gender
In this analysis, we examine attrition rates based on employee gender to identify whether there are differences in turnover between female and male employees. Answers are to 2 decimal places.
Female: (87/588)*100 = 14.80%
Male: (150/882)*100 = 17.01%
```sql
SELECT Gender, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, Gender
ORDER BY Gender, Attrition ASC;
```
- Male employees have a slightly higher attrition rate, which is expected given that there are more male employees in the dataset (882 males vs. 588 females, roughly a 1.5:1 ratio).
- When comparing attrition rates directly, male employees have an attrition rate of 17.01% versus 14.80% for female employees (approximately a 1.15:1 ratio).
- The difference is relatively small, suggesting that gender alone does not appear to be a significant factor in employee retention for this dataset.

#### Employee Attrition by age group
In this analysis, we examine attrition rates based on age groups to identify whether there are differences in turnover between employees of different ages. First, we have to create an age group column from the 'Age' column given.
```sql
# Create View for Age Group Summary 
CREATE VIEW age_group_summary AS
SELECT CASE
	WHEN Age >= 18 AND Age <= 25 THEN "18-25"
	WHEN Age >= 25 AND Age <= 30 THEN "25-30"
    WHEN Age >= 26 AND Age <= 40 THEN "26-40"
    ELSE "41-60"
END AS AgeGroup, Age, Department, EducationField, Gender, MaritalStatus, Attrition
FROM hr_employee_attrition;

# Testing of view
SELECT * FROM age_group_summary;

# No of employees per age group
SELECT AgeGroup, COUNT(*) AS no_of_employees
FROM age_group_summary
GROUP BY AgeGroup;
```
```sql
SELECT AgeGroup, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM age_group_summary
GROUP BY Attrition, AgeGroup
ORDER BY AgeGroup, Attrition ASC;
```
1. 18-25: (44/123)*100 = 35.77%
2. 25-30: (56/263)*100 = 21.29%
3. 26-40: (85/619)*100 = 13.73%
4. 41-60: (52/465)*100 = 11.18%
- Employees aged 18–25 (35.77%) have the highest attrition rate, suggesting younger workers are more likely to leave, possibly due to career exploration, short-term contracts, or pursuit of better opportunities.
- Ages 25–30 (21.29%) also show relatively high attrition, which may reflect employees seeking career advancement or higher pay after gaining some experience.
- Ages 26–40 (13.73%) and 41–60 (11.18%) have lower attrition rates, indicating that mid-career and older employees tend to be more stable, possibly due to stronger job commitment, family responsibilities, or satisfaction with their roles.

#### Employee Attrition by Educational Field
In this analysis, we examine attrition rates based on educational field to identify whether there are differences in turnover between employees of different academic backgrounds.
```sql
SELECT EducationField, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, EducationField
ORDER BY EducationField, Attrition ASC;
```
1. Human Resources: (7/27)*100 = 25.93%
2. Life Sciences: (89/606)*100 = 14.69%
3. Marketing: (35/159)*100 = 22.01%
4. Medical: (63/464)*100 = 13.58%
5. Technical Degree: (32/132)*100 =24.24%
6. Other: (11/82)*100 = 13.41%
- Human Resources (25.93%) and Technical Degrees (24.24%) have the highest attrition rates, suggesting employees from these fields may face strong external job opportunities or limited growth within the company.
- Marketing (22.01%) also shows relatively high turnover, which could be due to the fast-paced and competitive nature of the field, where job changes are common for career advancement.
- Life Sciences (14.69%), Medical (13.58%), and Other (13.41%) fields show lower attrition rates, likely reflecting greater job stability, specialised skills, or stronger commitment to their professions

#### Employee Attrition by Marital Status
In this analysis, we examine attrition rates based on marital status to identify whether there are differences in turnover between employees of different marital statuses. 
```sql
SELECT MaritalStatus, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, MaritalStatus
ORDER BY MaritalStatus, Attrition ASC;
```
1. Single: (120/470)*100 =25.53%
2. Married: (84/673)*100 = 12.48%
3. Divorced: (33/327)*100 = 10.09%
- Single employees (25.53%) have the highest attrition rate, suggesting they may be more likely to change jobs for better opportunities, relocation, or career growth since they often have fewer personal or family commitments.
- Married employees (12.48%) show a much lower attrition rate, possibly due to a greater desire for stability, financial security, and work-life balance.
- Divorced employees (10.09%) have the lowest attrition, which may reflect a stronger focus on job stability or established career roots.

### Job Info
#### Employee Attrition by Department
In this analysis, we examine attrition rates based on departments to identify whether there are differences in turnover between employees of different departments. 
```sql
SELECT Department, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, Department
ORDER BY Department, Attrition ASC;
```
1. Human Resources: (12/63)*100 = 19.05%
2. Research & Development: (133/961)*100 = 13.84%
3. Sales: (92/446)*100 = 20.63%
- Sales (20.63%) has the highest attrition rate, which may be linked to high performance pressure, frequent burnout, and the competitive nature of sales roles that often drive employees to switch companies for better pay or incentives.
- Human Resources (19.05%) also shows relatively high attrition, possibly due to limited advancement opportunities or HR professionals seeking new experiences in different organizations.
- Research & Development (13.84%) has the lowest attrition rate, suggesting that employees in this department may experience greater job satisfaction, strong engagement with their work, or more specialized skill requirements that promote stability.
  
#### Employee Attrition by Job Level
In this analysis, we examine attrition rates based on job levels to identify whether there are differences in turnover between employees of different job levels
```sql
SELECT JobLevel, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, JobLevel
ORDER BY JobLevel, Attrition ASC;
```
1. 1: (143/543)*100 = 26.34%
2. 2: (52/534)*100 = 9.74%
3. 3: (32/218)*100 = 14.68%
4. 4: (5/106)*100 = 4.72%
5. 5: (5/69)*100 = 7.25%
- Job Level 1 (26.34%) shows the highest attrition rate, indicating that entry-level employees are the most likely to leave, often due to limited experience, lower pay, or seeking better career opportunities.
- Job Level 2 (9.74%) and Level 3 (14.68%) have moderate attrition, suggesting that as employees gain experience, turnover decreases but may still occur due to career advancement or job dissatisfaction.
- Job Levels 4 (4.72%) and 5 (7.25%) have the lowest attrition, showing that senior and management-level employees tend to stay longer, likely due to higher job security, satisfaction, and organizational commitment.

#### Employee Attrition by Job Involvement
In this analysis, we examine attrition rates based on job involvement to identify whether there are differences in turnover between employees of different job involvement levels
```sql
SELECT JobInvolvement, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, JobInvolvement
ORDER BY JobInvolvement, Attrition ASC;
```
1. 1: (28/83)*100 = 33.73%
2. 2: (71/375)*100 = 18.93%
3. 3: (125/868)*100 = 14.40%
4. 4: (13/144)*100 = 9.03%
- Job Involvement Level 1 (33.73%) has the highest attrition rate, showing that employees with the lowest engagement are much more likely to leave. Low involvement often reflects weak connection to the job, low motivation, or lack of satisfaction.
- Levels 2 (18.93%) and 3 (14.40%) show moderate attrition, suggesting that as job involvement increases, turnover decreases.
- Level 4 (9.03%) has the lowest attrition rate, indicating that highly involved employees are the most likely to stay, likely because they are more motivated, satisfied, and committed to their roles.

#### Employee Attrition by Job Satisfaction
In this analysis, we examine attrition rates based on job satisfaction to identify whether there are differences in turnover between employees of different job satisfaction levels
```sql
SELECT JobSatisfaction, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, JobSatisfaction
ORDER BY JobSatisfaction, Attrition ASC;
```
1. 1: (66/289)*100 = 22.84%
2. 2: (46/280)*100 = 16.43%
3. 3: (73/442)*100 = 16.52%
4. 4: (52/459)*100 = 11.33%
- Job Satisfaction Level 1 (22.84%) has the highest attrition rate, showing that employees who are least satisfied with their jobs are the most likely to leave.
- Levels 2 (16.43%) and 3 (16.52%) show moderate attrition, suggesting that while somewhat satisfied employees are less likely to leave, there is still a notable risk of turnover if their needs aren’t met.
- Level 4 (11.33%) has the lowest attrition rate, indicating that highly satisfied employees are the most stable and committed to the organization.

### Financial Info
#### Employee Attrition by Monthly Income
In this analysis, we examine attrition rates based on monthly income.
```sql
CREATE OR REPLACE VIEW income_groups AS
SELECT
    EmployeeNumber,
    MonthlyIncome,
    Attrition,
    CASE
        WHEN MonthlyIncome BETWEEN 1000 AND 4999 THEN 'Low'
        WHEN MonthlyIncome BETWEEN 5000 AND 9999 THEN 'Medium'
        WHEN MonthlyIncome BETWEEN 10000 AND 14999 THEN 'High'
        WHEN MonthlyIncome BETWEEN 15000 AND 20000 THEN 'Very High'
        ELSE 'Other'
    END AS income_group
FROM hr_employee_attrition;

SELECT
    income_group,
    COUNT(*) AS employee_count,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_percentage
FROM income_groups
GROUP BY income_group
ORDER BY attrition_percentage DESC;
```
1. Low: 21.76%
2. Medium: 13.51%
3. High: 11.14%
4. Very High: 3.76%
- Low income (21.76%) has the highest attrition rate, suggesting that employees with lower pay are more likely to leave, possibly due to financial pressures or the pursuit of better-paying opportunities.
- Medium income (13.51%) and High income (11.14%) show moderate attrition, indicating that as monthly income increases, employees are generally more likely to stay.
- Very High income (3.76%) has the lowest attrition, reflecting that employees with the highest earnings are the most stable and committed, likely due to strong compensation and benefits.

#### Employee Attrition by Stock Level Options
In this analysis, we examine attrition rates based on stock level options:
```sql
SELECT StockOptionLevel, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, StockOptionLevel
ORDER BY StockOptionLevel, Attrition ASC;
```
1. 0: (154/631)*100 = 24.41%
2. 1: (56/596)*100 = 9.40%
3. 2: (12/158)*100 = 7.60%
4. 3: (15/85)*100 = 17.65%
- Employees with 0 stock options (24.41%) have the highest attrition rate, suggesting that not having equity or ownership incentives may make employees more likely to leave for opportunities that offer financial rewards or long-term benefits.
- Stock level 1 (9.40%) and level 2 (7.60%) show low attrition, indicating that even a small number of stock options may help increase retention.
- Stock level 3 (17.65%) is somewhat higher than levels 1 and 2, which could reflect a small sample size (85 employees), or that other factors beyond stock options (like role or satisfaction) affect turnover at this level.
