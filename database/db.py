import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("products.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER,
            product_id INTEGER,

            raw_price TEXT,
            raw_unit_price TEXT,
            price_per_100g REAL,

            scraped_at TEXT,

            FOREIGN KEY (store_id) REFERENCES stores(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()

def get_or_create_store(cur, name):
    cur.execute("SELECT id FROM stores WHERE name = ?", (name,))
    row = cur.fetchone()

    if row:
        return row[0]

    cur.execute("INSERT INTO stores (name) VALUES (?)", (name,))
    return cur.lastrowid

def get_or_create_product(cur, name):
    cur.execute("SELECT id FROM products WHERE name = ?", (name,))
    row = cur.fetchone()

    if row:
        return row[0]

    cur.execute("INSERT INTO products (name) VALUES (?)", (name,))
    return cur.lastrowid

def insert_price(conn, store_name, product_name, price_data):
    cur = conn.cursor()

    store_id = get_or_create_store(cur, store_name)
    product_id = get_or_create_product(cur, product_name)

    cur.execute(
        "INSERT INTO prices (store_id, product_id, raw_price, raw_unit_price, price_per_100g, scraped_at) VALUES (?, ?, ?, ?, ?, ?)",

        (
            store_id,
            product_id,
            price_data.get("price"),
            price_data.get("raw_unit_price"),
            price_data.get("price_per_100g"),
            datetime.now().isoformat()
        )
    )

    conn.commit()