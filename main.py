import sqlite3
from scrapers.tesco_scraper import scrape_tesco
from scrapers.sainsburys_scraper import scrape_sainsburys
from database.db import init_db, insert_price


def main():
    init_db()

    tesco_result = scrape_tesco()
    if tesco_result:
        conn = sqlite3.connect("products.db")
        insert_price(conn, "Tesco", "Brie", tesco_result)
        conn.close()

    sainsburys_result = scrape_sainsburys()
    if sainsburys_result:
        conn = sqlite3.connect("products.db")
        insert_price(conn, "Sainsburys", "Brie", sainsburys_result)
        conn.close()

if __name__ == "__main__":
    main()