from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from scrapers.find_price import find_price
from scrapers.find_price import find_unit_price
from database.normalize import normalize_unit_price


def scrape_sainsburys():
    url = "https://www.sainsburys.co.uk/groceries/product/sainsburys-somerset-brie-cheese-230g"
   
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    price_selectors = [
         (By.CSS_SELECTOR, "span.ds-c-price__price"),
         (By.CSS_SELECTOR, "span[class*='price__price']"),
    ]

    unit_price_selectors = [
         (By.CSS_SELECTOR, "span.ds-c-price__price-per-unit"),
         (By.CSS_SELECTOR, "span[class*='price-per-unit']"),
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
        print(f"sainsburys scraping failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    result = scrape_sainsburys()
    print(result)