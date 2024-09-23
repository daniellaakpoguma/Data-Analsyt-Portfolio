/*
 * A simple sales performance anlaysis of a supermarket 
 * Goal: To evaluate the sales performance on different metrics: brancg, prodyct lines, monthly, 
 */

 USE [supermarket-sales];
 -- KPI Generation
 -- Total Sales & Revenue
 SELECT SUM(Unit_Price*Quantity) AS Total_Sales, SUM(Gross_Income) AS Total_Profit
 FROM sales;

 -- Total Amount of Sales Per Branch
 SELECT COUNT(*) AS No_Of_Sales_A
 FROM sales
 WHERE Branch = 'A';

 SELECT COUNT(*) AS No_Of_Sales_B
 FROM sales
 WHERE Branch = 'B';

 SELECT COUNT(*) AS No_Of_Sales_C
 FROM sales
 WHERE Branch = 'C';

 -- Finding the number of different months and years of the dataset
 SELECT DISTINCT(YEAR(Date))
 FROM Sales;

 SELECT DISTINCT(MONTH(Date))
 FROM Sales;

 -- Total Sales & Revenuer Per Month
 SELECT SUM(Unit_Price*Quantity) AS Jan_Total_Sales, SUM(Gross_Income) AS Jan_Total_Profit
 FROM sales
 WHERE MONTH(Date) = 1; 

 SELECT SUM(Unit_Price*Quantity) AS Feb_Total_Sales, SUM(Gross_Income) AS Feb_Total_Profit
 FROM sales
 WHERE MONTH(Date) = 2; 

 SELECT SUM(Unit_Price*Quantity) AS Mar_Total_Sales, SUM(Gross_Income) AS Mar_Total_Profit
 FROM sales
 WHERE MONTH(Date) = 3; 

 -- Total Sales & Revenuer Per Branch
 SELECT SUM(Unit_Price*Quantity) AS Total_Sales_A, SUM(Gross_Income) AS Total_Profit_A
 FROM sales
 WHERE Branch = 'A';

 SELECT SUM(Unit_Price*Quantity) AS Total_Sales_B, SUM(Gross_Income) AS Total_Profit_B
 FROM sales
 WHERE Branch = 'B';

 SELECT SUM(Unit_Price*Quantity) AS Total_Sales_C, SUM(Gross_Income) AS Total_Profit_C
 FROM sales
 WHERE Branch = 'C';

 -- Top 10 Performing Sales
 SELECT TOP 10 *
 FROM sales
 ORDER BY Gross_Income DESC;

 -- Top 10 Least Performing Sales
 SELECT TOP 10 *
 FROM sales
 ORDER BY Gross_Income ASC;

  -- Top 10 Performing Sales By Branch
 SELECT TOP 10 *
 FROM sales
 WHERE Branch = 'A' 
 ORDER BY Gross_Income DESC;

 SELECT TOP 10 *
 FROM sales
 WHERE Branch = 'A' 
 ORDER BY Gross_Income ASC;

 SELECT TOP 10 *
 FROM sales
 WHERE Branch = 'B' 
 ORDER BY Gross_Income DESC;

 SELECT TOP 10 *
 FROM sales
 WHERE Branch = 'B' 
 ORDER BY Gross_Income ASC;

 SELECT TOP 10 *
 FROM sales
 WHERE Branch = 'C' 
 ORDER BY Gross_Income DESC;

 SELECT TOP 10 *
 FROM sales
 WHERE Branch = 'C' 
 ORDER BY Gross_Income ASC;

 -- Top Performing Sales By Product Line
 SELECT SUM (Gross_Income), Product_Line
 FROM sales
 GROUP BY  Product_Line;

SELECT A.Invoice_ID, B.Gross_Income, A.Branch AS Branch_A, B.Branch AS Branch_B
FROM sales A, sales B
WHERE A.Branch = 'A' AND B.Branch = 'B';

SELECT Unit_Price FROM Sales
UNION
SELECT Gross_Income FROM Sales;

SELECT AVG(Unit_Price) AS max_price, Branch
FROM sales
GROUP BY Branch
HAVING AVG(Unit_Price) > 50
ORDER BY max_price;





