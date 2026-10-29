"""Flask web integration: embeds the Tableau dashboard and story, plus a live SQL-backed KPI API."""
import sqlite3
from flask import Flask, render_template, jsonify
app = Flask(__name__)

# >>> Paste your Tableau Public URLs here (the "viz" part of the share link) <<<
DASHBOARD_URL = "https://public.tableau.com/views/YOUR_WORKBOOK/Dashboard"
STORY_URL     = "https://public.tableau.com/views/YOUR_WORKBOOK/Story"

def q(sql):
    con = sqlite3.connect("ev_market.db"); con.row_factory = sqlite3.Row
    rows = [dict(r) for r in con.execute(sql)]; con.close(); return rows

@app.route("/")
def home():
    kpi = q("""SELECT SUM(Annual_Sales) sales, COUNT(DISTINCT Manufacturer) manufacturers,
               ROUND(AVG(Range_km)) range, ROUND(AVG(Customer_Rating),2) rating FROM ev_market""")[0]
    return render_template("index.html", kpi=kpi, url=DASHBOARD_URL)

@app.route("/story")
def story(): return render_template("story.html", url=STORY_URL)

@app.route("/api/top-manufacturers")
def top(): return jsonify(q("SELECT * FROM v_manufacturer_summary ORDER BY total_sales DESC LIMIT 5"))

if __name__ == "__main__": app.run(debug=True)
