from playwright.sync_api import sync_playwright

def scrape_zalando_products(brand_slug: str):
    url = f"https://www.zalando.de/{brand_slug}-schuhe/"

    products = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )

            page = browser.new_page()
            page.goto(url, timeout=60000)

            page.wait_for_timeout(3000)

            # simple extraction fallback (no API dependency)
            items = page.query_selector_all("article")

            for item in items[:20]:
                try:
                    title = item.query_selector("h3")
                    price = item.query_selector("[data-testid='price']")

                    products.append({
                        "name": title.inner_text() if title else "Unknown",
                        "price": extract_price(price.inner_text() if price else None),
                        "url": url
                    })
                except:
                    continue

            browser.close()

    except Exception as e:
        print("Scraper error:", e)

    return products


def extract_price(text):
    try:
        if not text:
            return None
        return float(text.replace("€", "").replace(",", ".").strip())
    except:
        return None