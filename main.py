import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scrapers.sainsburys_scraper_cat import scrape_sainsburys_category
from scrapers.tesco_scraper_cat import scrape_tesco_category
from scrapers.paging import scrape_all_pages, scrape_all_pages_fresh, sainsburys_url, tesco_url
from database.db import init_db, insert_price
from config import SAINSBURYS_URLS, TESCO_URLS
import time
import random
import argparse
from database.filters import is_dairy


def make_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def run_sainsburys(conn):
    driver = make_driver()
    try:
        for base_url in SAINSBURYS_URLS:
            products = scrape_all_pages(
                driver, scrape_sainsburys_category, base_url, sainsburys_url, max_pages=4
            )
            products = [p for p in products if is_dairy(p["name"])]
            for p in products:
                insert_price(conn, "Sainsburys", p)
            print(f"Sainsburys: inserted {len(products)}")
    finally:
        driver.quit()


def run_tesco(conn, urls):
    for i, base_url in enumerate(urls):
        if i > 0:
            wait = random.uniform(30, 60)
            print(f"Waiting {wait:.0f}s before next category...")
            time.sleep(wait)

        products = scrape_all_pages_fresh(
            scrape_tesco_category, base_url, tesco_url, make_driver, max_pages=6
        )
        products = [p for p in products if is_dairy(p["name"])]
        for p in products:
            insert_price(conn, "Tesco", p)
        print(f"Tesco: inserted {len(products)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("store", choices=["sainsburys", "tesco"])
    parser.add_argument("--category", type=int, default=None,
                        help="index into TESCO_URLS (0 = first)")
    args = parser.parse_args()

    init_db()
    conn = sqlite3.connect("products.db")
    try:
        if args.store == "sainsburys":
            run_sainsburys(conn)
        else:
            urls = TESCO_URLS if args.category is None else [TESCO_URLS[args.category]]
            run_tesco(conn, urls)
    finally:
        conn.close()


if __name__ == "__main__":
    main()