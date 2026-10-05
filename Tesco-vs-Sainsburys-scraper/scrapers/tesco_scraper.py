from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from scrapers.find_price import find_price
from scrapers.find_price import find_unit_price
from database.normalize import normalize_unit_price


def scrape_tesco():
    url = "https://www.tesco.com/shop/en-GB/products/309188955"

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    price_selectors = [
        (By.CSS_SELECTOR, "p[class*='priceText']"),
        (By.CSS_SELECTOR, "p[class*='product-tile-price']"),
    ]

    unit_price_selectors = [
        (By.CSS_SELECTOR, "p[class*='unitPriceText']"),
        (By.CSS_SELECTOR, "p[class*='product-tile-unit-price']"),
   ]

    try:
            price = find_price(driver, price_selectors, timeout=10)
            unit_price = find_unit_price(driver, unit_price_selectors, timeout=10)
            print(f"Found price:{price}")
            print(f"Found unit price: {unit_price}")
            return {
                "price": price,
                "raw_unit_price": unit_price,
                "price_per_100g": normalize_unit_price(unit_price)
            }

    except ValueError as e:
        print(f"tesco scraping failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    result = scrape_tesco()
    print(result)