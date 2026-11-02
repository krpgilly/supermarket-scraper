import pandas as pd
import sqlite3
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
