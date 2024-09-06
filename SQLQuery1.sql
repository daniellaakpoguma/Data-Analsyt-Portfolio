/**
  * SQL Refresher Practice File 1
  **/

  /* Select all columns */
  SELECT * 
  FROM sales;

  /* Select particular columns */
  SELECT Branch, City 
  FROM sales;
  
  /* Find distinct values */
  SELECT DISTINCT Product_Line
  FROM sales;

  SELECT DISTINCT Payment
  FROM sales;

  SELECT DISTINCT City
  FROM sales
  
  SELECT DISTINCT Customer_Type
  FROM sales;
  
  /* Find Distinct count */
  SELECT COUNT(DISTINCT Product_Line)
  FROM sales;

  /* WHERE Clause */
  /* Find all Branch A Transactions */
  SELECT * 
  FROM sales
  WHERE Branch='A';

  /* Find Product Line used by Females */
  SELECT Invoice_ID, Product_Line
  FROM sales
  WHERE Gender='Female';

  /* Find Transactions with specified quantity */
  SELECT *
  FROM sales
  WHERE Quantity <= 3;

  SELECT *
  FROM sales
  WHERE Quantity BETWEEN 5 AND 10;

  SELECT *
  FROM sales
  WHERE YEAR(Date)=2019;

  SELECT *
  FROM sales
  WHERE MONTH(Date)=03;

  SELECT *
  FROM sales
  WHERE City LIKE 'N%';

  SELECT *
  FROM sales
  WHERE Product_Line IN ('Electronic accessories', 'Health and beauty');

  /* Order By */
  SELECT *
  FROM sales
  ORDER BY Unit_Price DESC;

  SELECT *
  FROM sales
  ORDER BY Customer_Type DESC;
    
  SELECT *
  FROM sales
  ORDER BY Gender ASC, Branch DESC;

  SELECT *
  FROM sales
  WHERE Gender='male' AND Product_Line='Home and lifestyle';


  SELECT COUNT(*) AS NUMBER
  FROM sales
  WHERE Gender='male' AND Product_Line='Home and lifestyle';

  SELECT * 
  FROM sales
  WHERE Branch='A' AND (Gender='male' OR Gender='FEMale');


  /* NOT Statememts */
  SELECT * 
  FROM sales
  WHERE NOT  Branch='A'
  ORDER BY Branch;

  SELECT * 
  FROM sales
  WHERE Payment NOT LIKE 'c%';

  SELECT * 
  FROM sales
  WHERE Quantity NOT BETWEEN 2 AND 10;

  SELECT * 
  FROM sales
  WHERE Branch NOT IN ('B', 'C');

  SELECT * 
  FROM sales
  WHERE NOT Quantity >= 5;

  SELECT * 
  FROM sales
  WHERE Branch IS NOT NULL;

  SELECT TOP 10 *
  FROM sales
  WHERE Branch IS NOT NULL;

  SELECT TOP 20 *
  FROM sales
  WHERE Branch = 'A'
  ORDER BY Quantity DESC;

  /* Aggregate Functions */
  SELECT MIN(Unit_Price)
  FROM sales
  WHERE Branch = 'A';

  SELECT MAX(Unit_Price)
  FROM sales
  WHERE Product_Line='Home and lifestyle';

  SELECT MIN(Unit_Price) AS Min_Price, Product_Line
  FROM sales
  WHERE Branch = 'A'
  GROUP BY Product_Line;

  SELECT COUNT(DISTINCT(Product_Line))
  FROM sales;

  
  SELECT SUM(Total) AS Total_Price, Branch
  FROM sales
  GROUP BY Branch;

  SELECT SUM(Total) AS Total_Price, Product_Line
  FROM sales
  GROUP BY Product_Line;

  SELECT SUM(Total*0.75) AS Total_Price_After_Tax, Product_Line
  FROM sales
  GROUP BY Product_Line;

  SELECT SUM(Total*Unit_Price) AS Total_Revenue, Product_Line
  FROM sales
  GROUP BY Product_Line;

  SELECT AVG(Unit_Price) AS Average_Price, Product_Line
  FROM sales
  GROUP BY Product_Line;

  SELECT *
  FROM sales
  WHERE Unit_Price < (SELECT AVG(Unit_Price) from sales);







  