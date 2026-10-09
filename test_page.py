from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from scrapers.find_price import find_price
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from scrapers.find_price import find_unit_price
from database.normalize import normalize_unit_price


def scrape_sainsburys_category(url):

    url = "https://www.sainsburys.co.uk/groceries/browse/chilled-food/dairy-and-chilled-essentials/c:1019022/brand:sainsbury%27s"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    # 1. wait until at least one card exists (use WebDriverWait + EC like before)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='gw-product-card']"))
        )
    except TimeoutException:
        print("Timeout occurred while waiting for product cards.")
        driver.quit()
        return []

    cards = driver.find_elements(By.CSS_SELECTOR, "[data-testid='gw-product-card']")
    products = []

    for card in cards:
        name = card.find_element(By.CSS_SELECTOR, "[data-testid='gw-product-name']").text.strip()

        # 2. get the shelf price from 'gw-product-retail-price', scoped to card
        price_el = card.find_elements(By.CSS_SELECTOR, "span.ds-c-price__price")
        price = price_el[0].text.strip() if price_el else None


        unit_price_el = card.find_elements(By.CSS_SELECTOR, "span.ds-c-price__price-per-unit")
        unit_price = unit_price_el[0].text.strip() if unit_price_el else None
        # 3. check for a deal: does card.find_elements(...) for
        #    'gw-product-contextual-price' come back non-empty? store True/False

        deal_el = card.find_elements(By.CSS_SELECTOR, "[data-testid='gw-product-contextual-price']")
        has_deal = len(deal_el) > 0


        products.append({"name": name, "retail_price": price, "unit_price": unit_price, "has_deal": has_deal})

    driver.quit()
    return products

if __name__ == "__main__":
    for p in scrape_sainsburys_category("PASTE_URL_HERE"):
        print(p)