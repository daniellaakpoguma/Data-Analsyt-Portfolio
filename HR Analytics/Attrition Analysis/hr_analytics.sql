USE hr_schema;

## DATA PREP
# Renaming Columns
ALTER TABLE hr_employee_attrition
RENAME COLUMN `ï»¿Age` to `Age`;

# Removing Duplicates
SELECT EmployeeNumber
FROM hr_employee_attrition
GROUP BY EmployeeNumber
HAVING COUNT(*) > 1;

# Deleting Redundant Columns
ALTER TABLE hr_employee_attrition
DROP COLUMN StandardHours;

ALTER TABLE hr_employee_attrition
DROP COLUMN Over18;

ALTER TABLE hr_employee_attrition
DROP COLUMN EmployeeCount;

## DATA UNDERSTANDING
# Total No of employees
SELECT COUNT(*) AS no_of_employees
FROM hr_employee_attrition;

# 1. Attrtiton Rate Overall
SELECT (CAST(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100 AS attrition_rate
FROM hr_employee_attrition;
# 2. Age General Stats
SELECT MIN(Age), MAX(Age), AVG(Age)
FROM hr_employee_attrition;
#3. No of employees by gender 
SELECT Gender, COUNT(*) AS no_of_employees
FROM hr_employee_attrition
GROUP BY Gender;
# 4. Average years at company
SELECT AVG(YearsAtCompany)  AS average_years_at_working
FROM hr_employee_attrition;
#5. Average monthly income
SELECT AVG(MonthlyIncome) AS avg_monthly_income
FROM  hr_employee_attrition;
#6. Most common job role
SELECT JobRole, COUNT(*)
FROM  hr_employee_attrition
GROUP BY JobRole;
#7. Most common education field
SELECT EducationField, COUNT(*) AS no_of_employees
FROM hr_employee_attrition
GROUP BY EducationField;

## ATTRITION INSIGHTS
## Personal Information
### Attrition by Gender
SELECT Gender, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, Gender
ORDER BY Gender, Attrition ASC;

### Attrition by Age Group
# Create view for Age Group Summary 
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
# Attrition by Age Group
SELECT AgeGroup, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM age_group_summary
GROUP BY Attrition, AgeGroup
ORDER BY AgeGroup, Attrition ASC;

### Attrition by Marital Status
SELECT MaritalStatus, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, MaritalStatus
ORDER BY MaritalStatus, Attrition ASC;

### Attrition by Educational Field
SELECT EducationField, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, EducationField
ORDER BY EducationField, Attrition ASC;

## Job Information
### Attrition by Department
SELECT Department, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, Department
ORDER BY Department, Attrition ASC;

### Attrition by Job Level
SELECT JobLevel, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, JobLevel
ORDER BY JobLevel, Attrition ASC;

### Attrition by Job Involvement
SELECT JobInvolvement, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, JobInvolvement
ORDER BY JobInvolvement, Attrition ASC;

### Attrition by Job Satisfaction
SELECT JobSatisfaction, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, JobSatisfaction
ORDER BY JobSatisfaction, Attrition ASC;

# Attrition by MonthlyIncome
SELECT  MonthlyIncome, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition,  MonthlyIncome
ORDER BY  MonthlyIncome, Attrition ASC;

# Attrition By Income Group
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

# Attrition by StockOptionLevel
SELECT StockOptionLevel, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, StockOptionLevel
ORDER BY StockOptionLevel, Attrition ASC;


DROP VIEW distancefromhome_summary;

CREATE VIEW distancefromhome_summary AS
SELECT 
  CASE 
    WHEN DistanceFromHome BETWEEN 0 AND 5 THEN '0-5 km'
    WHEN DistanceFromHome BETWEEN 6 AND 10 THEN '6-10 km'
    WHEN DistanceFromHome BETWEEN 11 AND 15 THEN '11-15 km'
    WHEN DistanceFromHome BETWEEN 16 AND 20 THEN '16-20 km'
    WHEN DistanceFromHome BETWEEN 21 AND 25 THEN '21-25 km'
    ELSE '26-30 km'
  END AS distance_group,
  Attrition,
  COUNT(*) AS employee_count
FROM hr_employee_attrition
GROUP BY distance_group, Attrition
ORDER BY distance_group;

# Attrition by Distance Frome Home
SELECT distance_group, Attrition, employee_count, ROUND(employee_count * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM distancefromhome_summary;

# Attrition by Performance Rating
SELECT PerformanceRating, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, PerformanceRating
ORDER BY PerformanceRating, Attrition ASC;

# Attrition by Gender & Marital Status
SELECT  MaritalStatus, Gender, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, MaritalStatus, Gender
ORDER BY MaritalStatus DESC, Gender, Attrition ASC;

# Attrition by BusinessTravel
SELECT  BusinessTravel, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, BusinessTravel
ORDER BY BusinessTravel, Attrition ASC;

# Attrition by OverTime
SELECT OverTime, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, OverTime
ORDER BY OverTime, Attrition ASC;

# Attrition by WorkLifeBalance
SELECT WorkLifeBalance, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, WorkLifeBalance
ORDER BY WorkLifeBalance, Attrition ASC;
