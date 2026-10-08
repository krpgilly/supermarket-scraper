from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re

def find_price(driver, selectors, timeout=10):
    """
    selectors: a list of tuples like (By.CSS_SELECTOR, "p[class*='priceText']")
    Tries each one in order. Returns the text of the first one that's found.
    Raises an exception if none of them work.
    """
    for by, sel in selectors:
        try:
            price_element = WebDriverWait(driver, timeout).until(
                   EC.presence_of_element_located((by, sel))
            )
            
            return price_element.text.strip()
            
        except TimeoutException:
            continue
    
    raise ValueError(f"None of the selectors worked: {selectors}")

def find_unit_price(driver, selectors, timeout=10):

    for by, sel in selectors:
        try:
            unit_price_element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, sel))
            )
            text = unit_price_element.text.strip()
            if re.search(r"£\s*\d+(\.\d+)?\s*/\s*\w+", text):
                return text
        except TimeoutException:
              continue

    raise ValueError(f"None of the selectors worked: {selectors}")
