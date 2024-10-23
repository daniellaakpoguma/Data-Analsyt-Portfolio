# Case Study #2 - Pizza Runner
## A. Pizza Metrics
1. How many pizzas were ordered?
``` sql
SELECT COUNT(*) AS no_of_pizza_orders
FROM pizza_runner.customer_orders;
```
2. How many unique customer orders were made?
``` sql
SELECT COUNT(DISTINCT(order_id)) AS customer_orders_count
FROM pizza_runner.customer_orders;
``` 
3. How many successful orders were delivered by each runner?
``` sql
SELECT COUNT(*) AS delivered_orders
FROM pizza_runner.runner_orders
WHERE cancellation IS NULL 
   OR cancellation = '' 
   OR cancellation = 'null';
``` 
4. How many of each type of pizza was delivered?
``` sql
SELECT o.pizza_id, pizza_name, COUNT(*) AS pizza_type_count
FROM pizza_runner.customer_orders AS o
JOIN pizza_runner.pizza_names AS n
ON o.pizza_id = n.pizza_id
GROUP BY o.pizza_id, pizza_name;
```

5. How many Vegetarian and Meatlovers were ordered by each customer?
``` sql
SELECT customer_id, pizza_name, COUNT(*) AS pizza_type_count
FROM pizza_runner.customer_orders AS o
JOIN pizza_runner.pizza_names AS n
ON o.pizza_id = n.pizza_id
GROUP BY customer_id, o.pizza_id, pizza_name
ORDER BY customer_id;
```

6. What was the maximum number of pizzas delivered in a single order?
``` sql
WITH count_of_pizza AS (
SELECT  order_id, COUNT(order_id) AS no_of_pizzas_in_order
FROM pizza_runner.customer_orders
GROUP BY order_id
) SELECT MAX (no_of_pizzas_in_order) AS max_no_pizzas
FROM count_of_pizza;
```

7. For each customer, how many delivered pizzas had at least 1 change and how many had no changes?
``` sql
/* Updating NULL values */
UPDATE pizza_runner.customer_orders
SET exclusions = NULL
WHERE exclusions = 'null' OR exclusions = '' ;

UPDATE pizza_runner.customer_orders
SET extras = NULL
WHERE extras = 'null' OR extras = '';

SELECT customer_id, COUNT(CASE WHEN  o.exclusions IS NULL AND  o.extras IS NULL THEN 1 END) as no_changes, COUNT(CASE WHEN   o.exclusions IS NOT NULL OR  o.extras IS NOT NULL THEN 1 END) as at_least_one_change
FROM pizza_runner.customer_orders AS o
GROUP BY customer_id;

```

8. How many pizzas were delivered that had both exclusions and extras?
``` sql
UPDATE pizza_runner.runner_orders
SET cancellation = NULL
WHERE cancellation = 'null' OR  cancellation = '';

SELECT COUNT(CASE WHEN o.exclusions IS NOT NULL AND  o.extras IS NOT NULL THEN 1 END) as pizzas_delivered_exclusions_extras
FROM pizza_runner.customer_orders AS o
JOIN pizza_runner.runner_orders AS r
ON o.order_id = r.order_id
WHERE cancellation IS  NULL;
```

9. What was the total volume of pizzas ordered for each hour of the day?
``` sql
SELECT EXTRACT(HOUR FROM CAST(o.order_time AS TIMESTAMP)) AS hour_of_the_day, COUNT(*) AS no_of_orders
FROM pizza_runner.customer_orders AS o
GROUP BY hour_of_the_day
ORDER BY hour_of_the_day;
```

10. What was the volume of orders for each day of the week?
``` sql
SELECT TO_CHAR(CAST(o.order_time AS TIMESTAMP), 'Day') AS day_of_the_week, 
       COUNT(*) AS no_of_orders
FROM pizza_runner.customer_orders AS o
GROUP BY TO_CHAR(CAST(o.order_time AS TIMESTAMP), 'Day')
ORDER BY day_of_the_week;
``` 

## B. Runner and Customer Experience
1. How many runners signed up for each 1 week period? (i.e. week starts 2021-01-01)
``` sql
SELECT FLOOR((registration_date - DATE '2021-01-01') / 7) + 1 AS week_no, COUNT(*) AS runner_count
FROM pizza_runner.runners
GROUP BY week_no
ORDER BY week_no;
```

2. What was the average time in minutes it took for each runner to arrive at the Pizza Runner HQ to pickup the order?
``` sql
/* Hanlde null string in table */
UPDATE pizza_runner.runner_orders
SET pickup_time = NULL
where pickup_time = 'null';

SELECT runner_id, AVG(CAST(pickup_time AS TIMESTAMP) - CAST(order_time AS TIMESTAMP)) AS avg_pickup_time
FROM pizza_runner.runner_orders r_info
JOIN pizza_runner.customer_orders orders
ON r_info.order_id = orders.order_id
GROUP BY runner_id;
```

3. Is there any relationship between the number of pizzas and how long the order takes to prepare?
``` sql
/** Query used in earlier questions to hanlde nulls string in table */
UPDATE pizza_runner.runner_orders
SET cancellation = NULL
WHERE cancellation = 'null' OR  cancellation = '';

/** Query used in earlier questions to hanlde nulls string in table */    
UPDATE pizza_runner.runner_orders
SET pickup_time = NULL
where pickup_time = 'null';

/** Answer for this question */
/* Assuming, the order is picked up as soon as the order is done being prepared */ 
 SELECT r.order_id, COUNT(*) AS no_of_pizzas_per_order, (CAST (pickup_time AS TIMESTAMP) - CAST(order_time AS TIMESTAMP)) AS prep_time
 FROM pizza_runner.customer_orders AS c
 JOIN pizza_runner.runner_orders AS r
 ON r.order_id = c.order_id
 WHERE cancellation IS  NULL
 GROUP BY r.order_id, prep_time
 ORDER BY  prep_time;
-- For the most part, the prep time is directly proportional to the number of pizzas in the order. However, there is a special case with order 8 which I thought was related to the type of pizza id or number of changes, but that also seems to not be the case
```
ANSWER: For the most part, the prep time is directly proportional to the number of pizzas in the order. However, there is a special case with order 8 which I thought was related to the type of pizza id or number of changes, but that also seems to not be the case

4. What was the average distance travelled for each customer?
``` sql
/** Excluding cancelled orders **/
SELECT customer_id,   AVG(CAST(NULLIF(REGEXP_REPLACE(distance, '[^0-9.]', '', 'g'), '') AS DECIMAL)) AS avg_distance
FROM pizza_runner.runner_orders AS r
JOIN  pizza_runner.customer_orders AS c
ON r.order_id = c.order_id
WHERE cancellation IS NULL
GROUP BY customer_id;
```

5. What was the difference between the longest and shortest delivery times for all orders?
``` sql
WITH cleaned_duration AS (
  SELECT (CAST(NULLIF(REGEXP_REPLACE(duration, '[^0-9.]', '', 'g'), '') AS 		DECIMAL)) AS numeric_duration
  FROM  pizza_runner.runner_orders
) 
SELECT MAX(numeric_duration) - MIN(numeric_duration) AS duration_difference
FROM cleaned_duration
```

6. What was the average speed for each runner for each delivery and do you notice any trend for these values?
``` sql
WITH cleaned_values AS (
  SELECT runner_id, order_id, (CAST(NULLIF(REGEXP_REPLACE(duration, '[^0-9.]', '', 'g'), '') AS 		DECIMAL)) AS numeric_duration, (CAST(NULLIF(REGEXP_REPLACE(distance, '[^0-9.]', '', 'g'), '') AS DECIMAL)) AS numeric_distance
  FROM  pizza_runner.runner_orders
  WHERE cancellation IS NULL
) SELECT runner_id, order_id, AVG(numeric_distance/numeric_duration) AS avg_speed
 FROM cleaned_values
 GROUP BY runner_id, order_id
 ORDER BY runner_id, order_id;
```

7. What is the successful delivery percentage for each runner?
``` sql
SELECT runner_id, COUNT(*) AS delivered_count
FROM pizza_runner.runner_orders
GROUP BY runner_id;
``` 

## C. Ingredient Optimisation
1. What are the standard ingredients for each pizza?
``` sql
WITH ingredients AS ( 
  SELECT  pizza_name, CAST(UNNEST(STRING_TO_ARRAY(toppings, ',')) AS INT) AS toppings_ids
  FROM pizza_runner.pizza_names AS n
  JOIN pizza_runner.pizza_recipes AS r
  ON n.pizza_id = r.pizza_id
  ) SELECT pizza_name, topping_name
  FROM ingredients AS i
  JOIN pizza_runner.pizza_toppings AS t
  ON i.toppings_ids = t.topping_id
  ORDER BY pizza_name;
```

2. What was the most commonly added extra?
``` sql
UPDATE pizza_runner.customer_orders
SET extras = NULL
WHERE extras  = 'null' OR  extras  = '';

WITH extras_ranking AS (
SELECT 
    CAST(extras_unnested AS INT) AS extras_single, 
    COUNT(*) AS count, 
    RANK() OVER (ORDER BY COUNT(*) DESC) AS rank
FROM (
    SELECT UNNEST(STRING_TO_ARRAY(extras, ',')) AS extras_unnested
    FROM pizza_runner.customer_orders
) AS unnested_extras
GROUP BY extras_single
) SELECT extras_single, count, rank
FROM extras_ranking
WHERE rank = 1;
 
```

3. What was the most common exclusion?
``` sql
UPDATE pizza_runner.customer_orders
SET extras = NULL
WHERE exclusions  = 'null' OR  exclusions  = '';

WITH exclusions_ranking AS (
SELECT 
    CAST(exclusions_unnested AS INT) AS exclusions_single, 
    COUNT(*) AS count, 
    RANK() OVER (ORDER BY COUNT(*) DESC) AS rank
FROM (
    SELECT UNNEST(STRING_TO_ARRAY(exclusions, ',')) AS exclusions_unnested
    FROM pizza_runner.customer_orders
) AS unnested_exclusions
GROUP BY exclusions_single
) SELECT exclusions_single, count, rank
FROM exclusions_ranking
WHERE rank = 1;
```

4. Generate an order item for each record in the customers_orders table in the format of one of the following:
a. Meat Lovers:
b. Meat Lovers - Exclude Beef:
c. Meat Lovers - Extra Bacon
d. Meat Lovers - Exclude Cheese, Bacon - Extra Mushroom, Peppers
``` sql
UPDATE pizza_runner.customer_orders
SET extras = NULL
WHERE extras  = 'null' OR  extras  = '';

UPDATE pizza_runner.customer_orders
SET extras = NULL
WHERE exclusions  = 'null' OR  exclusions  = '';

WITH orders_extras_exclusions AS (
  SELECT order_id, pizza_name, UNNEST(STRING_TO_ARRAY(extras, ',')) AS extras_unnested, UNNEST(STRING_TO_ARRAY(exclusions, ',')) AS exclusions_unnested
  FROM pizza_runner.pizza_names AS pizza_names
  JOIN pizza_runner.customer_orders AS orders
  ON orders.pizza_id = pizza_names.pizza_id
),
orders_extras_exclusions_names AS (
  SELECT order_id, pizza_name,
  CASE 
        WHEN extras_unnested IS NOT NULL AND extras_unnested <> '' 
  		THEN CAST(extras_unnested AS INT) 
        ELSE NULL 
        END AS extras_unnested,
   CASE 
         WHEN exclusions_unnested IS NOT NULL AND exclusions_unnested <> ''
  		 THEN CAST(exclusions_unnested AS INT) 
         ELSE NULL 
         END AS exclusions_unnested
  FROM orders_extras_exclusions
 ) 
 SELECT *
 FROM orders_extras_exclusions_names
 JOIN pizza_runner.pizza_toppings AS toppings 
  ON toppings.topping_id =  extras_unnested
  OR toppings.topping_id = exclusions_unnested
 WHERE extras_unnested IS NOT NULL OR  exclusions_unnested IS NOT NULL  ; 
```

5. Generate an alphabetically ordered comma separated ingredient list for each pizza order from the customer_orders table and add a 2x in front of any relevant ingredients. For example: "Meat Lovers: 2xBacon, Beef, ... , Salami"

6. What is the total quantity of each ingredient used in all delivered pizzas sorted by most frequent first?
``` sql
``` 

## D. Pricing and Ratings
1. If a Meat Lovers pizza costs $12 and Vegetarian costs $10 and there were no charges for changes - how much money has Pizza Runner made so far if there are no delivery fees?
2. What if there was an additional $1 charge for any pizza extras?
 - Add cheese is $1 extra
3. The Pizza Runner team now wants to add an additional ratings system that allows customers to rate their runner, how would you design an additional table for this new dataset - generate a schema for this new table and insert your own data for ratings for each successful customer order between 1 to 5.
4. Using your newly generated table - can you join all of the information together to form a table which has the following information for successful deliveries?
- customer_id
- order_id
- runner_id
- rating
- order_time
- pickup_time
- Time between order and pickup
- Delivery duration
- Average speed
- Total number of pizzas
5. If a Meat Lovers pizza was $12 and Vegetarian $10 fixed prices with no cost for extras and each runner is paid $0.30 per kilometre traveled - how much money does Pizza Runner have left over after these deliveries?

## E. Bonus Questions
If Danny wants to expand his range of pizzas - how would this impact the existing data design? Write an INSERT statement to demonstrate what would happen if a new Supreme pizza with all the toppings was added to the Pizza Runner menu?
