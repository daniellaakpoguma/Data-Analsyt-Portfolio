# HR Attrition Analysis
This project aims to calculate the rate at which employees leave an organisation and identify the possible underlying reasons for their departure.

## General Understanding
This project uses a fictitious dataset downloaded from Kaggle (https://www.kaggle.com/datasets/rishikeshkonapure/hr-analytics-prediction). There is a column, 'Attrition'  with Yes = Employees that have left the company,  No = Employees that are still at the company

## Attrition Analysis
### Employee Attrition at a general company level
The company has a general attrition rate of 16.12% percent, with 83.88% of employees staying.
```sql
SELECT Attrition, COUNT(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition;
```

### Employee Attrition by department
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

### Employee Attrition by gender
Female:  34.08 stay, 5.92 left = 5.76: 1 (588)
Male: 49.80 stay, 10.20 left = 4.88:1 (882 employees)

Takeaway: Female employees have a larger attrition rate, despite also being a limited number of employees
```sql
SELECT Gender, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM hr_employee_attrition
GROUP BY Attrition, Gender
ORDER BY Gender, Attrition ASC;
```

### Employee Attrition by age group
```sql
SELECT AgeGroup, Attrition, Count(*) AS employee_count, ROUND(COUNT(*) * 100.0 / (SELECT total_employees FROM total_employees), 2) AS percentage
FROM age_group_summary
GROUP BY Attrition, AgeGroup
ORDER BY AgeGroup, Attrition ASC;
```
