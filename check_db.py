import sqlite3

conn = sqlite3.connect("products.db")

for row in conn.execute("""
    SELECT s.name, p.name, pr.raw_price, pr.raw_unit_price
    FROM prices pr
    JOIN products p ON pr.product_id = p.id
    JOIN stores s ON pr.store_id = s.id
    WHERE s.name = 'Sainsburys'
    ORDER BY p.name
"""):
    print(row)

conn.close()