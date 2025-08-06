USE hr_schema;

ALTER TABLE hr_employee_attrition
RENAME COLUMN `ï»¿Age` to `Age`;

# General Stats
# No of employees
SELECT COUNT(*) AS no_of_employees
FROM hr_employee_attrition;

# No of employees per department
SELECT Department, COUNT(*) AS no_of_employees
FROM hr_employee_attrition
GROUP BY Department;

# Age General Stats
SELECT MIN(Age), MAX(Age), AVG(Age)
FROM hr_employee_attrition;

# Create view for Age Group Summary 
CREATE VIEW age_group_summary AS
SELECT CASE
	WHEN Age >= 18 AND Age <= 25 THEN "18-25"
	WHEN Age >= 25 AND Age <= 30 THEN "25-30"
    WHEN Age >= 26 AND Age <= 40 THEN "26-40"
    ELSE "41-60"
END AS AgeGroup, Age, Department, EducationField, Gender, MaritalStatus
FROM hr_employee_attrition;

# Testing of view
SELECT * FROM age_group_summary;

# No of employees per age group
SELECT AgeGroup, COUNT(*) AS no_of_employees
FROM age_group_summary
GROUP BY AgeGroup;

# No of employees per education field
SELECT EducationField, COUNT(*) AS no_of_employees
FROM hr_employee_attrition
GROUP BY EducationField;

# No of employees by gender 
SELECT Gender, COUNT(*) AS no_of_employees
FROM hr_employee_attrition
GROUP BY Gender;

## Comepensation Insights


