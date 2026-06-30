import asyncio
from playwright.async_api import async_playwright


async def scrape_products(brand_slug: str):

    url = f"https://www.zalando.de/{brand_slug}-schuhe/"
    products = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(4000)

        items = await page.query_selector_all("article")

        for item in items:
            try:
                name_el = await item.query_selector("h3")
                price_el = await item.query_selector("[data-test-id='product-price']")

                name = await name_el.inner_text() if name_el else None
                price_text = await price_el.inner_text() if price_el else None

                price = None
                if price_text:
                    price_text = price_text.replace("€", "").replace(",", ".")
                    try:
                        price = float(price_text.split()[0])
                    except:
                        price = None

                if name:
                    products.append({
                        "name": name,
                        "price": price,
                        "url": url
                    })

            except:
                continue

        await browser.close()

    return products