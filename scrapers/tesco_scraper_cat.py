from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from database.normalize import parse_unit_price

TESCO_DAIRY_URL = "https://www.tesco.com/shop/en-GB/browse/groceries-and-essentials/fresh-food/milk-butter-and-eggs/all?sortBy=relevance&facetsArgs=brands%3ATESCO%7C%7Cbrands%3ATESCO+finest%7C%7Cbrands%3ATESCO+ORGANIC&count=24#top"

def scrape_tesco_category(url=TESCO_DAIRY_URL):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul[data-testid='dynamic-grid'] > li"))
        )
    except TimeoutException:
        driver.quit()
        return []
    cards = driver.find_elements(By.CSS_SELECTOR, "ul[data-testid='dynamic-grid'] > li")
    print(len(cards))   # expect 24


    products = []
    for card in cards:
        link = card.find_element(By.CSS_SELECTOR, "a[class*='product-tile-product-link__link']")
        name = link.text.strip()
        product_url = link.get_attribute("href")

        price = card.find_element(By.CSS_SELECTOR, "p[class*='product-tile-price__text']").text.strip()
        unit_price = card.find_element(By.CSS_SELECTOR, "p[class*='product-tile-unit-price__subtext']").text.strip()

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

    driver.quit()
    return products

if __name__ == "__main__":
    for p in scrape_tesco_category(url=TESCO_DAIRY_URL):
        print(p)