# ⚡ Electric Vehicle Market Performance Insights

An end-to-end analytics project: **SQL database → Tableau dashboard & story → Flask web app**.

**Demo:** _add your Tableau Public / video link_ · **Author:** _your name_

## Problem Understanding
The EV industry produces large volumes of sales, battery, range, manufacturing and rating data. This project turns it into insights for three personas:
- **Emily Johnson (Market Strategy Director):** top categories, leading manufacturers, satisfaction by segment, battery adoption, growth segments.
- **David Chen (BI Manager):** manufacturer market share, manufacturing-country trends, dominant battery tech, ratings.
- **Dr. Sarah Williams (Research Analyst):** battery comparison, range improvement over time, global production, adoption drivers.

## Project Structure
```
data/generate_dataset.py   -> creates data/ev_market.csv (600 rows, synthetic)
load_to_db.py              -> cleans data + loads SQLite DB (ev_market.db) + views
sql/queries.sql            -> 8 analytical SQL queries
app.py, templates/, static -> Flask web integration (embeds Tableau)
```

## Run It
```bash
pip install -r requirements.txt
python data/generate_dataset.py      # or drop in your own ev_market.csv
python load_to_db.py
python app.py                        # http://127.0.0.1:5000
```

## Dataset Columns
Vehicle_ID, Manufacturer, Model, Category, Battery_Type, Battery_Capacity_kWh, Range_km, Price_USD, Annual_Sales, Manufacturing_Country, Customer_Rating, Charging_Time_Hrs, Year.
> The included data is **synthetic** (seeded, reproducible). Say so in your report, or swap in a real Kaggle EV dataset with the same columns.

## Milestone 1 – Data Collection & Extraction
1. Dataset collected as CSV (`data/ev_market.csv`).
2. Stored in SQLite via `load_to_db.py` (table `ev_market`, views `v_manufacturer_summary`, `v_category_summary`).
3. SQL operations in `sql/queries.sql` (aggregations, window function `LAG` for YoY growth, ranking).
4. **Connect to Tableau:** export tables to CSV, or use *Connect → To a Server → Other Databases (ODBC)* with a SQLite ODBC driver (or MySQL/PostgreSQL if you migrate). Tableau Public supports CSV/Excel only, so export `SELECT * FROM ev_market` to CSV for publishing.

## Milestone 2 – Data Preparation
Duplicates dropped on `Vehicle_ID`, nulls removed, invalid range/sales filtered (`load_to_db.py`). In Tableau confirm types: dimensions (Manufacturer, Category, Battery_Type, Country), measures (Sales, Range, Price, Rating), Year as Date/Discrete.

## Milestone 3 – Visualizations (build 10+ sheets)
| # | Sheet | Chart | Fields |
|---|---|---|---|
| 1 | Sales by Category | Bar | Category, SUM(Annual_Sales) |
| 2 | Top Manufacturers | Horizontal bar (Top 10 filter) | Manufacturer, SUM(Sales) |
| 3 | Market Share | Pie/Treemap | Manufacturer, % of Total Sales |
| 4 | Battery Adoption | Donut | Battery_Type, SUM(Sales) |
| 5 | Range by Category | Box plot | Category, Range_km |
| 6 | Sales Trend | Line | Year, SUM(Sales) by Category |
| 7 | Rating by Category | Highlight table | Category x Battery_Type, AVG(Rating) |
| 8 | Manufacturing Map | Filled map | Manufacturing_Country, SUM(Sales) |
| 9 | Price vs Range | Scatter | Price, Range, color=Battery_Type |
| 10 | Battery Capacity vs Range | Scatter + trend line | Capacity, Range |

**Calculated fields (Performance Testing criterion):**
```
Market Share %      = SUM([Annual_Sales]) / TOTAL(SUM([Annual_Sales]))
Range per $1000     = SUM([Range_km]) / (SUM([Price_USD])/1000)
YoY Growth %        = (SUM([Annual_Sales]) - LOOKUP(SUM([Annual_Sales]),-1)) / ABS(LOOKUP(SUM([Annual_Sales]),-1))
Rating Band         = IF AVG([Customer_Rating])>=4.3 THEN "Excellent" ELSEIF AVG([Customer_Rating])>=3.8 THEN "Good" ELSE "Needs Work" END
Charging Speed kW   = [Battery_Capacity_kWh] / [Charging_Time_Hrs]
Revenue (USD)       = [Annual_Sales] * [Price_USD]
```

## Milestone 4 – Dashboard
Combine sheets 1,2,4,6,8,9 plus KPI tiles (Total Sales, Avg Range, Avg Rating). Add **filters**: Year, Category, Battery_Type, Manufacturer, Country (apply to all worksheets; use filter actions). Set size to *Automatic* and build a **Phone layout** for responsiveness.

## Milestone 5 – Story (6 scenes)
1. Market overview (sales trend) → 2. Which categories drive sales → 3. Manufacturer leaders & market share → 4. Battery technology adoption → 5. Range & value comparison → 6. Manufacturing geography & ratings, with recommendations.

## Milestone 6 – Performance Testing
Record in your report: row count (600), number of filters (5), calculated fields (6), visualizations (10+). Use *Help → Settings and Performance → Start Performance Recording* and use extracts rather than live connections.

## Milestone 7 – Web Integration (Flask)
Publish to Tableau Public, copy each share link's URL, and paste into `DASHBOARD_URL` and `STORY_URL` in `app.py`. The home page also shows KPIs pulled live from the SQL database, and `/api/top-manufacturers` returns JSON.

## Milestone 8 – Demo & Documentation
Record a video covering problem → data → SQL → Tableau → Flask. Add the video link and this repo link on the SkillWallet project page.

## Push to GitHub
```bash
git init && git add . && git commit -m "EV Market Performance Insights"
git branch -M main
git remote add origin https://github.com/<you>/ev-market-insights.git
git push -u origin main
```
