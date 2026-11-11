import pandas as pd
import sqlite3
import rapidfuzz


def load_latest():
    conn = sqlite3.connect("products.db")
    df = pd.read_sql_query(
        """SELECT pr.id, s.name AS store, p.name AS product,
               pr.unit_value, pr.unit_type, pr.raw_price
        FROM prices pr
        JOIN products p ON pr.product_id = p.id
        JOIN stores s ON pr.store_id = s.id
""",
        conn,
    )

    conn.close()
    return df.sort_values("id").groupby(["store", "product"]).tail(1)


print(load_latest())
