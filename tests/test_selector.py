import pytest
from selenium.webdriver.common.by import By


SELECTOR_CASES = [
    pytest.param(
        "tesco",
        {
            "product": (By.CSS_SELECTOR, '[data-auto="product-tile"]'),
            "name": (By.CSS_SELECTOR, '[data-auto="product-tile--title"]'),
            "price": (By.CSS_SELECTOR, '[data-auto="price"]'),
        },
        id="tesco",
    ),
    pytest.param(
        "sainsburys",
        {
            "product": (By.CSS_SELECTOR, ".product-grid-box"),
            "name": (By.CSS_SELECTOR, ".product-grid-box__title"),
            "price": (By.CSS_SELECTOR, ".price__value"),
        },
        id="sainsburys",
    ),
]


def assert_valid_selector(selector):
    by, value = selector
    assert by in {
        By.ID,
        By.NAME,
        By.TAG_NAME,
        By.CLASS_NAME,
        By.CSS_SELECTOR,
        By.XPATH,
    }, f"Unsupported selector type: {by}"
    assert isinstance(value, str) and value.strip(), "Selector string is empty"


@pytest.mark.parametrize("store, selectors", SELECTOR_CASES)
def test_product_selector(store, selectors):
    assert_valid_selector(selectors["product"])
    assert selectors["product"][0] == By.CSS_SELECTOR, store


@pytest.mark.parametrize("store, selectors", SELECTOR_CASES)
@pytest.mark.parametrize("field", ("name", "price"))
def test_product_field_selectors(store, selectors, field):
    assert_valid_selector(selectors[field])
    assert selectors[field][0] == By.CSS_SELECTOR, f"{store} {field} selector type should be CSS selector"
