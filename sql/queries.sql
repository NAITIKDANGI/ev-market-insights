-- VIEWS (created on load)
CREATE VIEW IF NOT EXISTS v_manufacturer_summary AS
SELECT Manufacturer, SUM(Annual_Sales) total_sales, ROUND(AVG(Customer_Rating),2) avg_rating,
       ROUND(AVG(Range_km),0) avg_range,
       ROUND(100.0*SUM(Annual_Sales)/(SELECT SUM(Annual_Sales) FROM ev_market),2) market_share_pct
FROM ev_market GROUP BY Manufacturer;
CREATE VIEW IF NOT EXISTS v_category_summary AS
SELECT Category, SUM(Annual_Sales) total_sales, ROUND(AVG(Range_km),0) avg_range,
       ROUND(AVG(Customer_Rating),2) avg_rating FROM ev_market GROUP BY Category;
-- QUERIES
-- 1. Sales by category
SELECT Category, SUM(Annual_Sales) AS sales FROM ev_market GROUP BY Category ORDER BY sales DESC;
-- 2. Top 5 manufacturers
SELECT * FROM v_manufacturer_summary ORDER BY total_sales DESC LIMIT 5;
-- 3. Battery technology adoption
SELECT Battery_Type, COUNT(*) models, SUM(Annual_Sales) sales FROM ev_market GROUP BY Battery_Type ORDER BY sales DESC;
-- 4. Avg range by category and battery
SELECT Category, Battery_Type, ROUND(AVG(Range_km),0) avg_range FROM ev_market GROUP BY Category, Battery_Type;
-- 5. Manufacturing country distribution
SELECT Manufacturing_Country, COUNT(*) models, SUM(Annual_Sales) sales FROM ev_market GROUP BY 1 ORDER BY sales DESC;
-- 6. Year-over-year sales growth
SELECT Year, SUM(Annual_Sales) sales,
 ROUND(100.0*(SUM(Annual_Sales)-LAG(SUM(Annual_Sales)) OVER (ORDER BY Year))/LAG(SUM(Annual_Sales)) OVER (ORDER BY Year),1) yoy_pct
FROM ev_market GROUP BY Year;
-- 7. Customer satisfaction by category
SELECT Category, ROUND(AVG(Customer_Rating),2) rating FROM ev_market GROUP BY Category ORDER BY rating DESC;
-- 8. Best value: range per $1000
SELECT Model, Manufacturer, ROUND(Range_km/(Price_USD/1000.0),2) range_per_k FROM ev_market ORDER BY range_per_k DESC LIMIT 10;
