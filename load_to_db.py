"""Loads the CSV into SQLite (ev_market.db) and runs data-prep cleaning."""
import sqlite3, pandas as pd
df = pd.read_csv("data/ev_market.csv").drop_duplicates("Vehicle_ID").dropna()
df = df[(df.Range_km > 0) & (df.Annual_Sales > 0)]
con = sqlite3.connect("ev_market.db")
df.to_sql("ev_market", con, if_exists="replace", index=False)
con.executescript(open("sql/queries.sql").read().split("-- QUERIES")[0])  # views
print(f"Loaded {len(df)} rows into ev_market.db"); con.close()
