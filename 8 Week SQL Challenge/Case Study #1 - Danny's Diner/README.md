# Case Study #1 - Danny's Diner
### Case Study Questions
1. What is the total amount each customer spent at the restaurant?
```sql
SELECT customer_id, SUM(price) AS Total_Spent
FROM dannys_diner.sales AS sales JOIN dannys_diner.menu AS menu
ON sales.product_id = menu.product_id
GROUP BY customer_id;
```
2. How many days has each customer visited the restaurant?
```sql
SELECT customer_id, COUNT(DISTINCT(order_date)) AS No_Of_Days
FROM dannys_diner.sales
GROUP BY customer_id;
```
3. What was the first item from the menu purchased by each customer?
```sql
SELECT customer_id, MIN(order_date) AS first_order_date
FROM dannys_diner.sales
GROUP BY customer_id;
```
4. What is the most purchased item on the menu and how many times was it purchased by all customers?
```sql
SELECT sales.product_id, product_name, COUNT(*) AS No_Of_Times
FROM dannys_diner.sales AS sales JOIN dannys_diner.menu AS menu
ON sales.product_id = menu.product_id
GROUP BY sales.product_id, product_name
ORDER BY  No_Of_Times DESC LIMIT 1;
```
5. Which item was the most popular for each customer?
6. Which item was purchased first by the customer after they became a member?
7. Which item was purchased just before the customer became a member?
8. What is the total items and amount spent for each member before they became a member?
9. If each $1 spent equates to 10 points and sushi has a 2x points multiplier - how many points would each customer have?
10. In the first week after a customer joins the program (including their join date) they earn 2x points on all items, not just sushi - how many points do customer A and B have at the end of January?