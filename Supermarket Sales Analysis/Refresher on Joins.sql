USE olist_ecommerce_data;

SELECT Customers.customer_id, Customers.customer_zip_code_prefix, Orders.order_status
FROM [order_management].[orders] AS Orders
INNER JOIN [customers_and_sellers_management].[customers] AS Customers ON Orders.customer_id = Customers.customer_id;

SELECT Orders.order_id, Orders.customer_id, Orders.order_purchase_timestamp, Reviews.review_comment_title, Reviews.review_comment_message
FROM [order_management].[orders] AS Orders
INNER JOIN [order_management].[order_reviews] AS Reviews ON Orders.order_id = Reviews.order_id;

SELECT Orders.order_id, Customers.customer_zip_code_prefix,  Reviews.review_comment_title 
FROM [order_management].[orders] AS Orders
INNER JOIN [order_management].[order_reviews] AS Reviews ON Orders.order_id = Reviews.order_id
INNER JOIN [customers_and_sellers_management].[customers] AS Customers ON Orders.customer_id = Customers.customer_id;