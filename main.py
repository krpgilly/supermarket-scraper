import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scrapers.sainsburys_scraper_cat import scrape_sainsburys_category, SAINSBURYS_DAIRY_URL
from scrapers.tesco_scraper_cat import scrape_tesco_category, TESCO_DAIRY_URL
from scrapers.sainsburys_scraper_cat import scrape_sainsburys_category
from database.db import init_db, insert_price
from scrapers.paging import scrape_all_pages, sainsburys_url, tesco_url


def main(driver):
    init_db()

    sainsburys_products = scrape_all_pages(driver, scrape_sainsburys_category, SAINSBURYS_DAIRY_URL, sainsburys_url)
    if sainsburys_products:
        conn = sqlite3.connect("products.db")
        for product in sainsburys_products:
            insert_price(conn, "Sainsburys", product)
        conn.close()

    tesco_products = scrape_all_pages(driver, scrape_tesco_category, TESCO_DAIRY_URL, tesco_url)
    if tesco_products:
        conn = sqlite3.connect("products.db")
        for product in tesco_products:
            insert_price(conn, "Tesco", product)
        conn.close()

if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        main(driver)
    finally:
        driver.quit()