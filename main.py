import sqlite3
from scrapers.sainsburys_scraper_cat import scrape_sainsburys_category, SAINSBURYS_DAIRY_URL
from scrapers.tesco_scraper import scrape_tesco
from scrapers.sainsburys_scraper_cat import scrape_sainsburys_category
from database.db import init_db, insert_price


def main():
    init_db()

    tesco_result = scrape_tesco()
    if tesco_result:
        conn = sqlite3.connect("products.db")
        insert_price(conn, "Tesco", "Brie", tesco_result)
        conn.close()

    sainsburys_products = scrape_sainsburys_category(url=SAINSBURYS_DAIRY_URL)
    if sainsburys_products:
        conn = sqlite3.connect("products.db")
        for product in sainsburys_products:
            insert_price(conn, "Sainsburys", product)
        conn.close()

if __name__ == "__main__":
    main()