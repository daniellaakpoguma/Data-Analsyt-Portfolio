/* Specify Database */
USE poshmark_listings;

/* Perform operations on TOPS (1) */
ALTER TABLE tops
ADD Condition VARCHAR(50); -- Add Condition column if not exists

UPDATE tops
SET Condition = 
    CASE
        WHEN Description LIKE '%Like New%' THEN 'Like New'
        WHEN Description LIKE '%New%' THEN 'New'
		WHEN Description LIKE '%Not Used%' THEN 'New'
		WHEN Description LIKE '%Never Worn%' THEN 'New'
        WHEN Description LIKE '%Very Good%' THEN 'Very Good'
        WHEN Description LIKE '%Good%' THEN 'Good'
        WHEN Description LIKE '%Used%' THEN 'Used'
        WHEN Description LIKE '%Pre Loved%' THEN 'Used'
        ELSE 'N/A'
    END;

SELECT Description, Condition
FROM tops;

/* Perform operations on DRESSES (2)*/
ALTER TABLE dresses
ADD Condition VARCHAR(50); -- Add Condition column if not exists

UPDATE dresses
SET Condition = 
    CASE
         WHEN Description LIKE '%Like New%' THEN 'Like New'
        WHEN Description LIKE '%New%' THEN 'New'
		WHEN Description LIKE '%Not Used%' THEN 'New'
		WHEN Description LIKE '%Never Worn%' THEN 'New'
        WHEN Description LIKE '%Very Good%' THEN 'Very Good'
        WHEN Description LIKE '%Good%' THEN 'Good'
        WHEN Description LIKE '%Used%' THEN 'Used'
        WHEN Description LIKE '%Pre Loved%' THEN 'Used'
        ELSE 'N/A'
    END;

SELECT Description, Condition
FROM dresses;

/* Perform operations on PANTS  & JUMPSUITS (3)*/
ALTER TABLE pants_and_jumpsuits
ADD Condition VARCHAR(50); -- Add Condition column if not exists

UPDATE pants_and_jumpsuits
SET Condition = 
    CASE
        WHEN Description LIKE '%Like New%' THEN 'Like New'
        WHEN Description LIKE '%New%' THEN 'New'
		WHEN Description LIKE '%Not Used%' THEN 'New'
		WHEN Description LIKE '%Never Worn%' THEN 'New'
        WHEN Description LIKE '%Very Good%' THEN 'Very Good'
        WHEN Description LIKE '%Good%' THEN 'Good'
        WHEN Description LIKE '%Used%' THEN 'Used'
        WHEN Description LIKE '%Pre Loved%' THEN 'Used'
        ELSE 'N/A'
    END;

SELECT Description, Condition
FROM pants_and_jumpsuits;

/* Perform operations on SHORTS (4)*/
ALTER TABLE shorts
ADD Condition VARCHAR(50); -- Add Condition column if not exists

UPDATE shorts
SET Condition = 
    CASE
        WHEN Description LIKE '%Like New%' THEN 'Like New'
        WHEN Description LIKE '%New%' THEN 'New'
		WHEN Description LIKE '%Not Used%' THEN 'New'
		WHEN Description LIKE '%Never Worn%' THEN 'New'
        WHEN Description LIKE '%Very Good%' THEN 'Very Good'
        WHEN Description LIKE '%Good%' THEN 'Good'
        WHEN Description LIKE '%Used%' THEN 'Used'
        WHEN Description LIKE '%Pre Loved%' THEN 'Used'
        ELSE 'N/A'
    END;

SELECT Description, Condition
FROM shorts;

/* Perform operations on SHOES (5)*/
ALTER TABLE shoes
ADD Condition VARCHAR(50); -- Add Condition column if not exists

UPDATE shoes
SET Condition = 
    CASE
        WHEN Description LIKE '%Like New%' THEN 'Like New'
        WHEN Description LIKE '%New%' THEN 'New'
		WHEN Description LIKE '%Not Used%' THEN 'New'
		WHEN Description LIKE '%Never Worn%' THEN 'New'
        WHEN Description LIKE '%Very Good%' THEN 'Very Good'
        WHEN Description LIKE '%Good%' THEN 'Good'
        WHEN Description LIKE '%Used%' THEN 'Used'
        WHEN Description LIKE '%Pre Loved%' THEN 'Used'
        ELSE 'N/A'
    END;

SELECT Description, Condition
FROM shoes;

/* Perform operations on SHIRTS (6)*/
ALTER TABLE shirts
ADD Condition VARCHAR(50); -- Add Condition column if not exists

UPDATE shirts
SET Condition = 
    CASE
        WHEN Description LIKE '%Like New%' THEN 'Like New'
        WHEN Description LIKE '%New%' THEN 'New'
		WHEN Description LIKE '%Not Used%' THEN 'New'
		WHEN Description LIKE '%Never Worn%' THEN 'New'
        WHEN Description LIKE '%Very Good%' THEN 'Very Good'
        WHEN Description LIKE '%Good%' THEN 'Good'
        WHEN Description LIKE '%Used%' THEN 'Used'
        WHEN Description LIKE '%Pre Loved%' THEN 'Used'
        ELSE 'N/A'
    END;

SELECT Description, Condition
FROM shirts;

/* Perform operations on JEWELRY (7)*/
ALTER TABLE jewelry
ADD Condition VARCHAR(50); -- Add Condition column if not exists

UPDATE jewelry
SET Condition = 
    CASE
        WHEN Description LIKE '%Like New%' THEN 'Like New'
        WHEN Description LIKE '%New%' THEN 'New'
		WHEN Description LIKE '%Not Used%' THEN 'New'
		WHEN Description LIKE '%Never Worn%' THEN 'New'
        WHEN Description LIKE '%Very Good%' THEN 'Very Good'
        WHEN Description LIKE '%Good%' THEN 'Good'
        WHEN Description LIKE '%Used%' THEN 'Used'
        WHEN Description LIKE '%Pre Loved%' THEN 'Used'
        ELSE 'N/A'
    END;

SELECT Description, Condition
FROM jewelry;

/* Perform operations on INTIMATES AND SLEEPWEAR (8)*/
ALTER TABLE intimates_and_sleepwear
ADD Condition VARCHAR(50); -- Add Condition column if not exists

UPDATE intimates_and_sleepwear
SET Condition = 
    CASE
        WHEN Description LIKE '%Like New%' THEN 'Like New'
        WHEN Description LIKE '%New%' THEN 'New'
		WHEN Description LIKE '%Not Used%' THEN 'New'
		WHEN Description LIKE '%Never Worn%' THEN 'New'
        WHEN Description LIKE '%Very Good%' THEN 'Very Good'
        WHEN Description LIKE '%Good%' THEN 'Good'
        WHEN Description LIKE '%Used%' THEN 'Used'
        WHEN Description LIKE '%Pre Loved%' THEN 'Used'
        ELSE 'N/A'
    END;

SELECT Description, Condition
FROM intimates_and_sleepwear;

/* Perform operations on BAGS (9) */
ALTER TABLE bags
ADD Condition VARCHAR(50); -- Add Condition column if not exists

UPDATE bags
SET Condition = 
    CASE
        WHEN Description LIKE '%Like New%' THEN 'Like New'
        WHEN Description LIKE '%New%' THEN 'New'
		WHEN Description LIKE '%Not Used%' THEN 'New'
		WHEN Description LIKE '%Never Worn%' THEN 'New'
        WHEN Description LIKE '%Very Good%' THEN 'Very Good'
        WHEN Description LIKE '%Good%' THEN 'Good'
        WHEN Description LIKE '%Used%' THEN 'Used'
        WHEN Description LIKE '%Pre Loved%' THEN 'Used'
        ELSE 'N/A'
    END;

SELECT Description, Condition
FROM bags;

/* Perform operations on ACCESSORIES (10)*/
ALTER TABLE accessories
ADD Condition VARCHAR(50); -- Add Condition column if not exists

UPDATE accessories
SET Condition = 
    CASE
        WHEN Description LIKE '%Like New%' THEN 'Like New'
        WHEN Description LIKE '%New%' THEN 'New'
		WHEN Description LIKE '%Not Used%' THEN 'New'
		WHEN Description LIKE '%Never Worn%' THEN 'New'
        WHEN Description LIKE '%Very Good%' THEN 'Very Good'
        WHEN Description LIKE '%Good%' THEN 'Good'
        WHEN Description LIKE '%Used%' THEN 'Used'
        WHEN Description LIKE '%Pre Loved%' THEN 'Used'
        ELSE 'N/A'
    END;

SELECT Description, Condition
FROM accessories;

SELECT * 
FROM tops;

/* Most Expensive Brands in TOPS (1)*/
SELECT Brand, SUM(Price) AS Total_Prices
FROM tops
GROUP BY Brand
ORDER BY Total_Prices DESC;

/* Most Expensive Brands in SHORTS (2)*/
SELECT Brand, SUM(Price) AS Total_Prices
FROM shorts
GROUP BY Brand
ORDER BY Total_Prices DESC;

/* Most Expensive Brands in SHOES (3)*/
SELECT Brand, SUM(Price) AS Total_Prices
FROM shoes
GROUP BY Brand
ORDER BY Total_Prices DESC;

/* Most Expensive Brands in SHIRTS (4)*/
SELECT Brand, SUM(Price) AS Total_Prices
FROM shirts
GROUP BY Brand
ORDER BY Total_Prices DESC;

/* Most Expensive Brands in PANTS AND JUMPSUITS (5)*/
SELECT Brand, SUM(Price) AS Total_Prices
FROM pants_and_jumpsuits
GROUP BY Brand
ORDER BY Total_Prices DESC;

/* Most Expensive Brands in JEWELRY (6)*/
SELECT Brand, SUM(Price) AS Total_Prices
FROM jewelry
GROUP BY Brand
ORDER BY Total_Prices DESC;

/* Most Expensive Brands in INTIMATES (7)*/
SELECT Brand, SUM(Price) AS Total_Prices
FROM intimates_and_sleepwear
GROUP BY Brand
ORDER BY Total_Prices DESC;

/* Most Expensive Brands in DRESSES(8)*/
SELECT Brand, SUM(Price) AS Total_Prices
FROM dresses
GROUP BY Brand
ORDER BY Total_Prices DESC;

/* Top Performing Brands in BAGS(9)*/
SELECT Brand, SUM(Price) AS Total_Prices
FROM bags
GROUP BY Brand
ORDER BY Total_Prices DESC;

/* Most Expensive Brands in ACCESSORIES(10)*/
SELECT Brand, SUM(Price) AS Total_Prices
FROM accessories
GROUP BY Brand
ORDER BY Total_Prices DESC;

