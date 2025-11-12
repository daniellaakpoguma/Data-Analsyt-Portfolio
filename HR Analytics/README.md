# HR Attrition Analysis
Employee turnover is a major cost for organisations. Understanding which employees are at higher risk of leaving allows HR to implement targeted retention strategies. This project aims to do just that by calculating the rate at which employees leave an organisation and identifying the possible underlying reasons for their departure.

![Cover Image](images/cover_image.png)

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
![Employee Number](images/general_employee_count.png)
```sql
SELECT COUNT(*) AS no_of_employees
FROM hr_employee_attrition;
```
- Attrition Rate Overall: 16.12%
![General Attrition](images/general_employee_count.png)
```sql
SELECT (CAST(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100 AS attrition_rate
FROM hr_employee_attrition;
```
- Min, Max and Avg Age of Employees:
![ages](images/min-max-avg-age.png)
```sql
SELECT MIN(Age), MAX(Age), AVG(Age)
FROM hr_employee_attrition;
```
- Gender distribution: 882 Male, 588 Female
![Gender Distribution](images/employees_by_gender.png)
```sql
# No of employees by gender 
SELECT Gender, COUNT(*) AS no_of_employees
FROM hr_employee_attrition
GROUP BY Gender;
```
- No of employees by gender
```sql
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
```sql
SELECT JobRole, COUNT(*)
FROM  hr_employee_attrition
GROUP BY JobRole;
```
- Most common education field: Life Sciences
![Education Field Distribution](images/no_of_employees_education_field.png)
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
- Human Resources: (7/27)*100 = 25.93%
- Life Sciences: (89/606)*100 = 14.69%
- Marketing: (35/159)*100 = 22.01%
- Medical: (63/464)*100 = 13.58%
- Technical Degree: (32/132)*100 =24.24%
- Other: (11/82)*100 = 13.41%
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
- Single: (120/470)*100 =25.53%
- Married: (84/673)*100 = 12.48%
- Divorced: (33/327)*100 = 10.09%
- Single employees (25.53%) have the highest attrition rate, suggesting they may be more likely to change jobs for better opportunities, relocation, or career growth since they often have fewer personal or family commitments.
- Married employees (12.48%) show a much lower attrition rate, possibly due to a greater desire for stability, financial security, and work-life balance.
- Divorced employees (10.09%) have the lowest attrition, which may reflect a stronger focus on job stability or established career roots.

### Job Info
#### Employee Attrition by department
There are three departments of varying sizes, with Research & Development being the highest, so best is ratio (sTAY-TO-LEAVE)rounded to 2 decimals:
Research & Development: 56.33: 9.05 = 6.22 : 1
Sales: 24.08: 6.26 = 3.85 : 1
Human Resources: 3.47: 0.82  = 4.23 : 1

1. Research & Development (961 employees) has the highest stay-to-leave ratio (6.22:1), which reflects strong retention overall. Given its large workforce, the attrition observed here is not alarming.
2, Human Resources (63 employees) shows a moderate ratio (4.23:1). While the absolute number of leavers is small, the impact on such a small department can be significant, making attrition here more concerning.
3. Sales (442 employees) has the lowest ratio (3.85:1), indicating higher relative attrition compared to the other departments. Given its mid-size workforce, this trend could point to structural or cultural issues that warrant closer attention.

Takeaway: Although attrition in Research & Development is highest in absolute terms, the real concern lies in Sales and Human Resources, where smaller team sizes magnify the effect of employee departures.

```sql
SELECT Department, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, Department
ORDER BY Department, Attrition ASC;
```
#### Employee Attrition by Job Level
5 job levels, stay-to-leave ratio.
1: 27.21: 9.73 = 2.80: 1 (543)
2: 32.79 / 3.54 = 9.26:1 (534)
3: 12.65 : 2.18 = 5.80 (218)
4 : 6.87:0.34 = 20.20 (106)
5: 4.35: 0.34 = 12.79 (69)

This is unique out of all the sector where have done, where as the job level with the least amount of employees are the ones seeing higher attrition levels.

```sql
SELECT JobLevel, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, JobLevel
ORDER BY JobLevel, Attrition ASC;
```

#### Employee Attrition by Job Involvement
1: 83 employees. 3.74:1.90 = 1.97
2: 375 employees. 20.68:4.83 = 4.28
3: 868 employees. 50.54:8.50 = 5.95
4: 144 employees. 8.91:0.88 = 10.125 

i think i did the wrong thing. and smaller values are considered employees leaving faster. i shoud use (left/total in that level)

```sql
SELECT JobInvolvement, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, JobInvolvement
ORDER BY JobInvolvement, Attrition ASC;
```
