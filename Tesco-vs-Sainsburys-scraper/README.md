# Tesco vs Sainsburys Price Comparison

A beginner-friendly Python project that compares supermarket prices by converting each product to a common value: price per 100g. That lets you compare Tesco and Sainsburys fairly, even when the products come in different weights or pack sizes.

This keeps the comparison focused on actual value rather than marketing pack size.

## What This Does

The project scrapes a fixed Brie product page from Tesco and Sainsburys. It saves the displayed item price and unit price, then normalizes the unit price into one metric: price per 100g. The current scraper does not extract the product weight separately.

That makes it easier to see which supermarket is offering better value for the same product, even when the packaging is different.

The app also stores the results in a local SQLite database so the raw item price, raw unit price, and normalized price per 100g are saved. This makes it easy to review the source data and the calculated value side by side.

---

## What Is Working Now

The main workflow is working through `main.py`.

When you run it, the app attempts to:

- create or update the database tables
- pull data from the Tesco scraper
- pull data from the Sainsburys scraper
- store each result in SQLite
- save the raw price, unit price, normalized price, and timestamp

The scraper uses fixed product URLs and Selenium with Chrome. Successful scraping depends on the pages being reachable and their markup matching the configured selectors.

---

## Key Engineering Decisions

### Fallback Selectors for Resilience

Web scraping is fragile. A tiny change in a website layout can break a selector. To make the scrapers more reliable, each one tries a few possible selectors instead of relying on a single one.

```python
price_selectors = [
    (By.CSS_SELECTOR, "p[class*='priceText']"),
    (By.CSS_SELECTOR, "p[class*='product-tile-price']"),
]

unit_price_selectors = [
    (By.CSS_SELECTOR, "p[class*='unitPriceText']"),
    (By.CSS_SELECTOR, "p[class*='product-tile-unit-price']"),
]
```

The Tesco scraper passes these selector lists to `find_price()` and `find_unit_price()`. Each helper checks selectors in order; if none yields a matching value, it raises an error rather than silently returning missing data.

### Price Normalization

The standalone `normalize_price()` function handles item prices such as "£2.50" or "45p" and weights such as "200g", "1.5kg", or "1000mg". The live scrapers currently call `normalize_unit_price()` instead: it converts displayed unit prices in `/100g` or `/kg` format into price per 100g. For example:

```text
£0.82/100g → 0.82
£8.20/kg   → 0.82
```

Both functions are covered by the normalization tests, but only `normalize_unit_price()` is used in the current scraping flow. The displayed unit price must be in one of its supported formats for normalization to succeed.

### Database Schema: Raw + Computed Values

The database keeps both the original scraped values and the calculated values:

```sql
CREATE TABLE prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER,
    product_id INTEGER,

    raw_price TEXT,
    raw_unit_price TEXT,
    price_per_100g REAL,

    scraped_at TEXT,

    FOREIGN KEY (store_id) REFERENCES stores(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

This is helpful because if the normalization logic changes later, the original scraped values remain available. You can always recalculate and compare old data without losing the source information.

---

## Setup & Running

### Prerequisites

You need Python 3.7+ and pip.

### 1. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

On Mac/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install selenium webdriver-manager
```

- **selenium**: browser automation for scraping pages
- **webdriver-manager**: downloads and manages the correct Chrome driver automatically

### 3. Initialize the Database

```bash
python -m database.db
```

This creates `products.db` in the project root and sets up the tables for stores, products, and prices.

### 4. Run the Project

```bash
python main.py
```

This is the main entry point. It runs the scraping flow, saves data to SQLite, and updates the current price comparison data.

If you want to run an individual scraper manually, the project still supports that pattern too.

---

## Project Structure

```text
database/
  db.py              # database setup and insert logic
  normalize.py       # price normalization and unit conversion

scrapers/
  find_price.py      # selector fallback logic
  sainsburys_scraper.py  # Sainsburys scraper
  tesco_scraper.py   # Tesco scraper

tests/
  test_database.py   # checks that stores, products, and price data are saved correctly
  test_normalize.py  # checks for edge cases in the price calculation
  test_selector.py   # validates the Tesco and Sainsburys HTML selectors used by the scrapers

main.py              # main app entry point; works and stores results
README.md            # project overview
```

---

## Planned JSON API

The basic idea behind the project is still the same: collect prices from supermarkets, normalize them, and make the comparison easy to use.

The next useful step is a simple JSON API that exposes the saved data in a clean format.

This would let you:

- return product comparison data as JSON
- query prices across both stores for one item
- see historical price changes over time

Why this is a good next step:

1. **Accessibility**: JSON is easier for scripts, apps, and websites to consume than reading SQLite directly.
2. **Separation**: the scraper can keep doing its job while the API simply serves the stored results.
3. **Extensibility**: once the data is in JSON, it is easier to build a small frontend or a more advanced product tracker later.

An example of the kind of output we want:

```bash
GET /api/compare?product=brie&store=sainsburys,tesco
→ {
    "product": "brie",
    "results": [
      {"store": "sainsburys", "price_per_100g": 0.82, "scraped_at": "2026-08-14T10:30:00"},
      {"store": "tesco", "price_per_100g": 0.95, "scraped_at": "2026-08-14T10:30:00"}
    ]
  }
```

This is still a future step, but it fits the same project scope: the scraper gathers the numbers, the database stores them, and the API would just make them easier to use.

---

## Testing

Run the tests to check both the price conversion logic and the database insert workflow:

```bash
python -m pytest tests/ -v
```

The database test uses an in-memory SQLite database, so it checks that:

- store and product records are created
- raw price and unit price values are saved
- the normalized price per 100g is saved
- a scrape timestamp is added

The normalize tests check the price conversion logic, including different currency and weight formats, invalid values, and zero-weight protection.

The selector tests check that the example selector values in `tests/test_selector.py` are non-empty CSS selector strings. They do not inspect the live selectors configured in either scraper, parse selectors for CSS validity, or check them against current supermarket pages.

If needed, install pytest first:

```bash
pip install pytest
```

---

## Current Status & Next Steps

The project is now in a stronger position than before:

- `main.py` runs the pipeline for fixed Brie product pages, provided the pages and selectors are available
- the database schema is storing products, stores, and prices separately
- the comparison logic is tied to real saved data
- the JSON API is still the next natural layer to build on top of that data

Possible future improvements include:

- better Tesco and Sainsburys selectors and anti-bot handling
- product matching for more than hardcoded examples
- scheduled scraping for price history
- a simple frontend or API dashboard

---

## Why This Matters

Supermarket pricing can be confusing. A product can look cheap because of its pack size, but the real value is in the price per 100g. This project makes that comparison easier and more transparent.

It is useful for budgeting, checking value, and understanding whether supermarkets are making the real cost harder to compare.
