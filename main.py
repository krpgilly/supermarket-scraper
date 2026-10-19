import sqlite3
from scrapers.sainsburys_scraper_cat import scrape_sainsburys_category, SAINSBURYS_DAIRY_URL
from scrapers.tesco_scraper_cat import scrape_tesco_category, TESCO_DAIRY_URL
from scrapers.sainsburys_scraper_cat import scrape_sainsburys_category
from database.db import init_db, insert_price


def main():
    init_db()

    sainsburys_products = scrape_sainsburys_category(url=SAINSBURYS_DAIRY_URL)
    if sainsburys_products:
        conn = sqlite3.connect("products.db")
        for product in sainsburys_products:
            insert_price(conn, "Sainsburys", product)
        conn.close()

    tesco_products = scrape_tesco_category(url=TESCO_DAIRY_URL)
    if tesco_products:
        conn = sqlite3.connect("products.db")
        for product in tesco_products:
            insert_price(conn, "Tesco", product)
        conn.close()

if __name__ == "__main__":
    main() 
    