A. Customer Journey
Based off the 8 sample customers provided in the sample from the subscriptions table, write a brief description about each customer’s onboarding journey.
Try to keep it as short as possible - you may also want to run some sort of join to make your explanations a bit easier!

B. Data Analysis Questions
1. How many customers has Foodie-Fi ever had?
``` sql
SELECT COUNT(DISTINCT(customer_id)) AS no_customers
FROM foodie_fi.subscriptions;
```
2. What is the monthly distribution of trial plan start_date values for our dataset - use the start of the month as the group by value
``` sql
SELECT DATE_TRUNC('month',start_date) AS month, COUNT(*)
FROM foodie_fi.subscriptions
GROUP BY month
ORDER BY month;
```
3. What plan start_date values occur after the year 2020 for our dataset? Show the breakdown by count of events for each plan_name
``` sql
SELECT plan_name, COUNT(*)
FROM foodie_fi.subscriptions AS s
JOIN foodie_fi.plans AS p
ON s.plan_id = p.plan_id
WHERE DATE_TRUNC('year',start_date) > '2020-01-01'
GROUP BY plan_name;
```

4. What is the customer count and percentage of customers who have churned rounded to 1 decimal place?
``` sql
SELECT plan_name, (COUNT(DISTINCT(customer_id) * 1.0)/customer_count) AS churn_percent
FROM foodie_fi.plans AS p
JOIN (
  SELECT plan_id, customer_id, COUNT(DISTINCT(customer_id)) AS customer_count           FROM foodie_fi.subscriptions 
  GROUP BY plan_id, customer_id
  ) AS c
ON s.plan_id = p.plan_id
JOIN foodie_fi.subscriptions AS s 
ON s.plan_id = p.plan_id
WHERE plan_name = 'churn'
GROUP BY plan_name, c.customer_count;

SELECT 
    p.plan_name, 
    (COUNT(DISTINCT s.customer_id) * 1.0) / total_customers.total_count AS churn_percent
FROM 
    foodie_fi.plans AS p
JOIN foodie_fi.subscriptions AS s ON s.plan_id = p.plan_id
JOIN (
    SELECT 
        COUNT(DISTINCT customer_id) AS total_count
    FROM 
        foodie_fi.subscriptions
) AS total_customers ON 1=1
WHERE 
    p.plan_name = 'churn'
GROUP BY 
    p.plan_name, total_customers.total_count;
``` 
5. How many customers have churned straight after their initial free trial - what percentage is this rounded to the nearest whole number?
6. What is the number and percentage of customer plans after their initial free trial?
7. What is the customer count and percentage breakdown of all 5 plan_name values at 2020-12-31?
8. How many customers have upgraded to an annual plan in 2020?
9. How many days on average does it take for a customer to an annual plan from the day they join Foodie-Fi?
10. Can you further breakdown this average value into 30 day periods (i.e. 0-30 days, 31-60 days etc)
11. How many customers downgraded from a pro monthly to a basic monthly plan in 2020?