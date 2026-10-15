from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from database.normalize import parse_unit_price


SAINSBURYS_DAIRY_URL = "https://www.sainsburys.co.uk/groceries/browse/chilled-food/dairy-and-chilled-essentials/c:1019022/brand:sainsbury%27s"

def scrape_sainsburys_category(url=SAINSBURYS_DAIRY_URL):

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

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

        prices = card.find_elements(By.CSS_SELECTOR, "span.ds-c-price__price")
        units = card.find_elements(By.CSS_SELECTOR, "span.ds-c-price__price-per-unit")

        if len(prices) == 2:
            deal_price, deal_unit = prices[0].text.strip(), units[0].text.strip()
            price, unit_price = prices[1].text.strip(), units[1].text.strip()
        else:
            price, unit_price = prices[0].text.strip(), units[0].text.strip()
            deal_price = deal_unit = None

        has_deal = deal_price is not None
        parsed = parse_unit_price(unit_price)
        unit_value, unit_type = parsed if parsed else (None, None)

        deal_value, deal_type = (None, None)
        if deal_unit:
            parsed_deal = parse_unit_price(deal_unit)
            if parsed_deal:
                deal_value, deal_type = parsed_deal

        products.append({
            "name": name,
            "retail_price": price,
            "unit_price": unit_price,
            "deal_price": deal_price,
            "deal_unit_price": deal_unit,
            "has_deal": has_deal,
            "unit_value": unit_value,
            "unit_type": unit_type,
            "deal_unit_value": deal_value,
            "deal_unit_type": deal_type,
        })
    driver.quit()
    return products

if __name__ == "__main__":
    url = "https://www.sainsburys.co.uk/groceries/browse/chilled-food/dairy-and-chilled-essentials/c:1019022/brand:sainsbury%27s"
    for p in scrape_sainsburys_category(url):
        print(p)