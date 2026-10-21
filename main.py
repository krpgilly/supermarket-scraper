import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scrapers.sainsburys_scraper_cat import scrape_sainsburys_category, SAINSBURYS_DAIRY_URL
from scrapers.tesco_scraper_cat import scrape_tesco_category, TESCO_DAIRY_URL
from scrapers.paging import scrape_all_pages, scrape_all_pages_fresh, sainsburys_url, tesco_url
from database.db import init_db, insert_price


def make_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def main(driver):
    init_db()

    sainsburys_products = scrape_all_pages(
        driver, scrape_sainsburys_category, SAINSBURYS_DAIRY_URL, sainsburys_url, max_pages=3
    )

    tesco_products = scrape_all_pages_fresh(
        scrape_tesco_category, TESCO_DAIRY_URL, tesco_url, make_driver, max_pages=4
    )

    conn = sqlite3.connect("products.db")
    for p in sainsburys_products:
        insert_price(conn, "Sainsburys", p)
    for p in tesco_products:
        insert_price(conn, "Tesco", p)
    conn.close()


if __name__ == "__main__":
    driver = make_driver()
    try:
        main(driver)
    finally:
        driver.quit()