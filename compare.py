# STEP 1: Import required libraries (pandas, sqlite3/sqlalchemy, and a fuzzy matching library like rapidfuzz)
# STEP 2: Establish a connection to the database ('products.db')
# STEP 3: Write SQL queries to extract the required tables (Names, Prices, Discount Prices, Prices Per Unit)
# STEP 4: Load the SQL data into separate Pandas DataFrames
# STEP 5: Close the database connection
# STEP 6: Clean and preprocess the data (e.g., standardise text to lowercase, strip extra spaces, handle missing values)

# STEP 7: Merge the dataframes together on a common key (like Product ID) so all details are in one main DataFrame
# STEP 8: Define a fuzzy matching function to calculate similarity scores between product names
# STEP 9: Loop or apply the fuzzy matching function across the products to compare them and find close matches
# STEP 10: Filter and inspect the results to see which products are potential duplicates or matches
import os
import pandas as pd
import sqlite3
from rapidfuzz import fuzz, process
from database.categories import categorise

def load_latest():
    conn = sqlite3.connect('products.db')
    df = pd.read_sql_query("""SELECT pr.id, s.name AS store, p.name AS product,
               pr.unit_value, pr.unit_type, pr.raw_price
        FROM prices pr
        JOIN products p ON pr.product_id = p.id
        JOIN stores s ON pr.store_id = s.id
""", conn)

    conn.close()
    return df.sort_values("id").groupby(["store", "product"]).tail(1)

if __name__ == "__main__":
    df = load_latest()
    df["category"] = df["product"].apply(categorise)
    coverage = df.dropna(subset=["category"]).groupby(["category", "store"]).size().unstack("store").fillna(0)
    print(coverage)

    matched = df.dropna(subset=["category"])

table = (
    matched.groupby(["category", "unit_type", "store"])["unit_value"]
    .mean()
    .unstack("store")
    .dropna()
    .round(3)
)
table["cheaper"] = table.apply(
    lambda r: "Sainsburys" if r["Sainsburys"] < r["Tesco"] else "Tesco", axis=1
)
print(table)
