# Tesco vs Sainsbury's Price Scraper

A Python project that scrapes grocery category pages from Tesco and Sainsbury's and stores product prices in a local SQLite database. It keeps the displayed prices and unit prices, along with parsed unit values, so products can be compared using a common unit where possible.

## What It Does

Running `main.py` performs these steps in order:

1. Creates the `stores`, `products`, and `prices` tables in `products.db` if they do not already exist.
2. Opens the configured Sainsbury's dairy and chilled category page and collects its product cards.
3. Saves each returned Sainsbury's product and its price data.
4. Opens the configured Tesco milk, butter, and eggs category page and collects its product cards.
5. Saves each returned Tesco product and its price data.

The category URLs are defined by `SAINSBURYS_DAIRY_URL` in `scrapers/sainsburys_scraper_cat.py` and `TESCO_DAIRY_URL` in `scrapers/tesco_scraper_cat.py`. Both scrapers use Selenium to drive Chrome and `webdriver-manager` to obtain ChromeDriver. The page structure and selectors are specific to the current supermarket websites, so website changes or access restrictions can prevent a scrape from succeeding.

If a scraper times out waiting for product cards, it returns an empty list and the pipeline continues to the next store. Products are only inserted when the scraper returns results.

## Data Collected

Each product record is keyed by its name. Each scrape can add a price row containing the displayed retail price and unit-price text, the parsed unit value and type, available deal fields, and the scrape timestamp. The database schema also stores a reference to the store and product.

The unit parser supports unit prices per `kg`, `100g`, `ltr`/`litre`, `100ml`, and `ea`/`each`. It converts these to comparable values per `100g`, per `100ml`, or per item, and records the corresponding unit type. Not every product can therefore be compared directly: the unit types must match.

Sainsbury's scraper extracts deal price and deal unit-price values when the product card exposes them. The Tesco scraper currently returns a promotional text field, but `main.py`/`insert_price()` do not store that text or populate Tesco deal-price fields.

The database retains raw price strings as well as parsed values:

```sql
CREATE TABLE prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER,
    product_id INTEGER,
    raw_price TEXT,
    raw_unit_price TEXT,
    unit_value REAL,
    unit_type TEXT,
    deal_price TEXT,
    raw_deal_unit_price TEXT,
    deal_unit_value REAL,
    deal_unit_type TEXT,
    has_deal INTEGER,
    scraped_at TEXT
);
```

Each run appends price records; it does not overwrite historical rows or match equivalent products across stores. Products with different names are stored as separate products.

## Setup and Running

### Prerequisites

- Python and pip
- Google Chrome

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install selenium webdriver-manager
```

To run the test suite, install pytest as well:

```bash
pip install pytest
```

### 3. Run the scraper

From the project root:

```bash
python main.py
```

The database is created automatically in the project root as `products.db`. To initialize it without scraping:

```bash
python -m database.db
```

## Project Structure

```text
database/
  db.py                       # SQLite schema and insert functions
  normalize.py                # Unit-price parsing and normalization

scrapers/
  find_price.py               # Fallback helpers used by the individual-product scrapers
  sainsburys_scraper_cat.py   # Sainsbury's category scraper used by main.py
  sainsburys_scraper_sing.py  # Individual Sainsbury's product scraper
  tesco_scraper_cat.py        # Tesco category scraper used by main.py
  tesco_scraper.py            # Individual Tesco product scraper

tests/
  test_database.py            # Database insert behavior
  test_normalize.py           # Price and unit parsing behavior
  test_selector.py            # Checks example selector definitions

main.py                       # Runs both category scrapers and saves their results
products.db                   # Local SQLite database, created when the app runs
```

The individual-product scrapers and `find_price.py` remain in the repository, but they are not called by the current `main.py` workflow.

## Testing

Run the tests from the project root:

```bash
python -m pytest tests/ -v
```

The database tests check that store, product, and price records are inserted. The normalization tests cover supported price and unit formats. The selector tests validate example selector strings; they do not verify the live selectors used by the category scrapers or test them against supermarket pages.

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
GET /api/compare?product=brie&store=lidl,tesco
→ {
    "product": "brie",
    "results": [
      {"store": "lidl", "price_per_100g": 0.82, "scraped_at": "2026-08-14T10:30:00"},
      {"store": "tesco", "price_per_100g": 0.95, "scraped_at": "2026-08-14T10:30:00"}
    ]
  }
```

This is still a future step, but it fits the same project scope: the scraper gathers the numbers, the database stores them, and the API would just make them easier to use.

## Current Limitations and Possible Next Steps

- The category URLs and selectors are fixed in the scraper modules.
- A scrape depends on Chrome being available, the sites being reachable, and their page markup remaining compatible with the selectors.
- Product matching between supermarkets is not implemented.
- Tesco promotional text is scraped but is not currently stored in the database.
- Each run adds price history, but there is no query interface or scheduled scraper.

A future JSON API or small dashboard could expose historical prices and compare products after product matching is added.
