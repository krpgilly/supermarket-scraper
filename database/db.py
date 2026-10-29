import sqlite3
from datetime import datetime
from database.filters import is_dairy

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
            unit_value REAL,
            unit_type TEXT,

            deal_price TEXT,
            raw_deal_unit_price TEXT,
            deal_unit_value REAL,
            deal_unit_type TEXT,
            has_deal INTEGER,

            scraped_at TEXT,

            FOREIGN KEY (store_id) REFERENCES stores(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        );
    """)

    conn.commit()
    conn.close()

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

def insert_price(conn, store_name, price_data):
    cur = conn.cursor()

    store_id = get_or_create_store(cur, store_name)
    product_id = get_or_create_product(cur, price_data["name"])


    cur.execute("""
        SELECT 
            raw_price, raw_unit_price, unit_value, unit_type,
            deal_price, raw_deal_unit_price,
            deal_unit_value, deal_unit_type, has_deal
        FROM prices
        WHERE store_id = ? AND product_id = ?
        ORDER BY id DESC
        LIMIT 1
        """, (store_id, product_id),
    )
    latest = cur.fetchone()

    new = (
        price_data.get("retail_price"),
        price_data.get("raw_unit_price"),
        price_data.get("unit_price"),
        price_data.get("unit_value"),
        price_data.get("unit_type"),
        price_data.get("deal_price"),
        price_data.get("deal_unit_price"),
        price_data.get("deal_unit_value"),
        price_data.get("deal_unit_type"),
        1 if price_data.get("has_deal") else 0,
    )

    if latest == new:
        return False
    
    cur.execute(
        """
        INSERT INTO prices (
            store_id, product_id,
            raw_price, raw_unit_price, unit_value, unit_type,
            deal_price, raw_deal_unit_price, deal_unit_value, deal_unit_type,
            has_deal, scraped_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            store_id,
            product_id,
            price_data.get("retail_price"),
            price_data.get("unit_price"),
            price_data.get("unit_value"),
            price_data.get("unit_type"),
            price_data.get("deal_price"),
            price_data.get("deal_unit_price"),
            price_data.get("deal_unit_value"),
            price_data.get("deal_unit_type"),
            1 if price_data.get("has_deal") else 0,
            datetime.now().isoformat(),
        ),
    )

    conn.commit()
    return True

if __name__ == "__main__":
    init_db()
