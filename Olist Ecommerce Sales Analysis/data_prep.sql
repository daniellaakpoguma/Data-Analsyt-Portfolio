-- Schema and Table Preparation

-- Create schema for customer and seller management
CREATE SCHEMA customers_and_sellers_management;
-- Create schema for order management
CREATE SCHEMA order_management;
-- Create schema for product management
CREATE SCHEMA product_management;
-- Create schema for geolocation management
CREATE SCHEMA geolocation_management;

-- Create Primary Keys
-- Primary key for Customers Table
ALTER TABLE customers_and_sellers_management.customers
ADD PRIMARY KEY(customer_id);

-- Primary key for Sellers Table
ALTER TABLE customers_and_sellers_management.sellers
ADD PRIMARY KEY(seller_id);

-- Primary key for Orders Table
ALTER TABLE order_management.orders
ADD PRIMARY KEY(order_id);

-- Composite Primary Key for Order Items Table
ALTER TABLE order_management.order_items
ADD CONSTRAINT PK_order_item PRIMARY KEY (order_item_id, order_id);

-- Foreign key for Orders Payment Table
-- First converted Order_ID to VARCHAR to match orders table
ALTER TABLE order_management.order_payments
ALTER COLUMN order_id VARCHAR(50); 

ALTER TABLE order_management.order_payments
ADD CONSTRAINT FK_order_payments_order
FOREIGN KEY (order_id) REFERENCES order_management.orders (order_id);


-- Find Duplicates
SELECT review_id, COUNT(*)
FROM order_management.order_reviews
GROUP BY review_id
HAVING COUNT(*) > 1;

-- Remove Duplicates
WITH CTE AS (
    SELECT review_id,
           ROW_NUMBER() OVER (
               PARTITION BY review_id 
               ORDER BY 
                   CASE WHEN review_comment_title IS NOT NULL THEN 1 ELSE 0 END DESC,
                   CASE WHEN review_comment_message IS NOT NULL THEN 1 ELSE 0 END DESC,
                   (SELECT NULL)
           ) AS rn
    FROM order_management.order_reviews
)
DELETE FROM CTE
WHERE rn > 1;

-- Primary key for Orders Reviews Table
ALTER TABLE order_management.order_reviews
ADD PRIMARY KEY(review_id);

-- Primary key for Product Table
ALTER TABLE product_management.products
ADD PRIMARY KEY(product_id);

-- Foreign Key For Order Reviews table
ALTER TABLE order_management.order_reviews
ALTER COLUMN order_id VARCHAR(50); 

ALTER TABLE order_management.order_reviews
ADD CONSTRAINT FK_order_reviews_order
FOREIGN KEY (order_id) REFERENCES order_management.orders (order_id);

-- Primary key for Geolocation Table
ALTER TABLE geolocation_management.geolocations
ADD PRIMARY KEY(geolocation_zip_code_prefix);