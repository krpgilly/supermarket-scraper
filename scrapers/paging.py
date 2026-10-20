import time
import random

def sainsburys_url(base, page):
    return base if page == 1 else f"{base}/opt/page:{page}"

def tesco_url(base, page):
    if page == 1:
        return base
    return base.replace("sortBy=relevance", f"sortBy=relevance&page={page}")


def scrape_all_pages(driver, scrape_fn, base_url, build_url, max_pages=20):
    all_products = []
    seen = set()

    for page in range(1, max_pages + 1):
        products = scrape_fn(driver, build_url(base_url, page))

        if not products:
            break

        new = [p for p in products if p["name"] not in seen]
        if not new:          # page of repeats, so we've run past the end
            break

        seen.update(p["name"] for p in new)
        all_products.extend(new)
        print(f"page {page}: {len(new)} new products")
        time.sleep(random.uniform(15, 25))

    return all_products