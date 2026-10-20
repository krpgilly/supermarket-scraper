import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from database.normalize import parse_unit_price

TESCO_DAIRY_URL = "https://www.tesco.com/shop/en-GB/browse/groceries-and-essentials/fresh-food/milk-butter-and-eggs/all?sortBy=relevance&facetsArgs=brands%3ATESCO%7C%7Cbrands%3ATESCO+finest%7C%7Cbrands%3ATESCO+ORGANIC&count=24#top"

def tiles_ready(driver):
    cards = driver.find_elements(By.CSS_SELECTOR, "ul[data-testid='dynamic-grid'] > li")
    if not cards:
        return False
    links = driver.find_elements(By.CSS_SELECTOR, "ul[data-testid='dynamic-grid'] > li a[class*='product-tile-product-link__link']")
    units = driver.find_elements(By.CSS_SELECTOR, "ul[data-testid='dynamic-grid'] > li p[class*='product-tile-unit-price__subtext']")
    return len(links) >= len(cards) and len(units) >= len(cards)

def scrape_tesco_category(driver, url=TESCO_DAIRY_URL):

    for attempt in range(2):
        driver.get(url)
        try:
            WebDriverWait(driver, 60).until(tiles_ready)
            break
        except TimeoutException:
            print(f"Tiles not ready (attempt {attempt + 1})")

    if "access denied" in driver.title.lower() or "access denied" in driver.page_source[:2000].lower():
        print("Blocked by Tesco, stopping")
        return []
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #time.sleep(2)
    #driver.execute_script("window.scrollTo(0, 0);")

    try:
        WebDriverWait(driver, 60).until(tiles_ready)
    except TimeoutException:
        print("Tiles never fully rendered")
    cards = driver.find_elements(By.CSS_SELECTOR, "ul[data-testid='dynamic-grid'] > li")
    print(len(cards))   # expect 24
    print(cards[0].get_attribute("outerHTML")[:2000])

    products = []
    for card in cards:
        price_els = card.find_elements(By.CSS_SELECTOR, "p[class*='product-tile-price__text']")
        unit_els = card.find_elements(By.CSS_SELECTOR, "p[class*='product-tile-unit-price__subtext']")
        link_els = card.find_elements(By.CSS_SELECTOR, "a[class*='product-tile-product-link__link']")

        if not price_els or not unit_els or not link_els:
            print("Skipping card:", card.text[:80].replace("\n", " | "))
            continue

        link = link_els[0]
        name = link.text.strip()
        product_url = link.get_attribute("href")
        price = price_els[0].text.strip()
        unit_price = unit_els[0].text.strip()

        promo_els = card.find_elements(By.CSS_SELECTOR, "p[class*='value-bar__content-text']")
        promo_text = promo_els[0].text.strip() if promo_els else None

        parsed = parse_unit_price(unit_price)
        unit_value, unit_type = parsed if parsed else (None, None)
        products.append({
            "name": name,
            "url": product_url,
            "retail_price": price,
            "unit_price": unit_price,
            "unit_value": unit_value,
            "unit_type": unit_type,
            "promo_text": promo_text,
        })

    return products

if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        for p in scrape_tesco_category(driver, url=TESCO_DAIRY_URL):
            print(p)
    finally:
        driver.quit()