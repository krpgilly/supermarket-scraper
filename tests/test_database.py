import sqlite3
import pytest
from database.db import init_db, insert_price

@pytest.fixture
def memory_db(monkeypatch):
    db_uri = "file:test_products?mode=memory&cache=shared"

    real_connect = sqlite3.connect  
    anchor_conn = real_connect(db_uri, uri=True)

    monkeypatch.setattr(
        "sqlite3.connect",
        lambda path, *args, **kwargs: real_connect(db_uri, uri=True)
    )
    init_db()

    yield anchor_conn

    anchor_conn.close()

def test_insert_price_creates_records_and_saves_data(memory_db):
    store_name = "Sainsburys"
    product_name = "Brie"
    mock_price_data = {
        "name": "Brie",
        "retail_price": "£1.65",
        "unit_price": "82.5p per 100g",
        "unit_value": 0.82,
        "unit_type": "100g",
        "deal_price": None,
        "deal_unit_price": None,
        "deal_unit_value": None,
        "deal_unit_type": None,
        "has_deal": False
    }
    
    insert_price(memory_db, store_name, mock_price_data)
    
    cur = memory_db.cursor()

    cur.execute("SELECT id, name FROM stores WHERE name = ?", (store_name,))
    store_record = cur.fetchone()
    assert store_record is not None, "Store record was not created."
    assert store_record[1] == "Sainsburys"
    
    cur.execute("SELECT id, name FROM products WHERE name = ?", (product_name,))
    product_record = cur.fetchone()
    assert product_record is not None, "Product record was not created."
    assert product_record[1] == "Brie"
    
    cur.execute("""
        SELECT store_id, product_id, raw_price, raw_unit_price, unit_value, scraped_at 
        FROM prices
    """)
    price_record = cur.fetchone()
    
    assert price_record is not None, "Price data was never written to the prices table."
    assert price_record[0] == store_record[0]    
    assert price_record[1] == product_record[0] 
    assert price_record[2] == "£1.65"         
    assert price_record[3] == "82.5p per 100g"    
    assert price_record[4] == 0.82          
    assert price_record[5] is not None

SAMPLE = {
    "name": "Test Mature Cheddar 400g",
    "retail_price": "£2.95",
    "unit_price": "£7.38 / kg",
    "unit_value": 0.738,
    "unit_type": "100g",
    "deal_price": None,
    "deal_unit_price": None,
    "deal_unit_value": None,
    "deal_unit_type": None,
    "has_deal": False,
}


def count_rows():
    conn = sqlite3.connect("products.db")
    n = conn.execute("SELECT COUNT(*) FROM prices").fetchone()[0]
    conn.close()
    return n


def test_unchanged_price_not_inserted(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    init_db()
    conn = sqlite3.connect("products.db")

    assert insert_price(conn, "Sainsburys", SAMPLE) is True
    assert insert_price(conn, "Sainsburys", SAMPLE) is False
    conn.close()

    assert count_rows() == 1


def test_changed_unit_price_inserts_new_row(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    init_db()
    conn = sqlite3.connect("products.db")

    insert_price(conn, "Sainsburys", SAMPLE)
    changed = {**SAMPLE, "unit_value": 0.80, "retail_price": "£3.20"}
    assert insert_price(conn, "Sainsburys", changed) is True
    conn.close()

    assert count_rows() == 2