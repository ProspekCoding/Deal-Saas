from playwright.sync_api import sync_playwright

def scrape_zalando_products_sync(brand_slug: str):
    url = f"https://www.zalando.de/{brand_slug}-schuhe/"

    products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000)
        page.wait_for_timeout(5000)

        # scroll to load products
        for _ in range(5):
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(1000)

        # extract product cards
        cards = page.query_selector_all("article")

        for card in cards:
            try:
                name_el = card.query_selector("a")
                price_el = card.query_selector("[data-testid*='price']")
                discount_el = card.query_selector("[data-testid*='discount']")

                name = name_el.inner_text() if name_el else None
                url = name_el.get_attribute("href") if name_el else None

                price_text = price_el.inner_text() if price_el else None
                discount_text = discount_el.inner_text() if discount_el else ""

                price = None
                if price_text:
                    price = float(
                        price_text.replace("€", "")
                        .replace(",", ".")
                        .split()[0]
                    )

                if name and url:
                    products.append({
                        "name": name,
                        "url": "https://www.zalando.de" + url,
                        "price": price,
                        "discount": discount_text
                    })

            except:
                continue

        browser.close()

    return products