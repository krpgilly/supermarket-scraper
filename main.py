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


def make_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def main(driver):
    init_db()
    conn = sqlite3.connect("products.db")

    driver = make_driver()
    try:
        for base_url in SAINSBURYS_URLS:
            products = scrape_all_pages(
                driver, scrape_sainsburys_category, base_url, sainsburys_url, max_pages=4
            )
            for p in products:
                insert_price(conn, "Sainsburys", p)
            print(f"Sainsburys: inserted {len(products)}")
    finally:
        driver.quit()

    for base_url in TESCO_URLS:
        products = scrape_all_pages_fresh(
            scrape_tesco_category, base_url, tesco_url, make_driver, max_pages=13
        )
        for p in products:
            insert_price(conn, "Tesco", p)
        print(f"Tesco: inserted {len(products)}")
        time.sleep(random.uniform(30, 60))   
    conn.close()


if __name__ == "__main__":
    driver = make_driver()
    try:
        main(driver)
    finally:
        driver.quit()