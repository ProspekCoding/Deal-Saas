from app.scraper_zalando import scrape_zalando_products_sync

# in-memory price history (for MVP)
previous_prices = {}

def check_brand(brand_slug: str):
    products = scrape_zalando_products_sync(brand_slug)

    alerts = []

    for p in products:
        url = p.get("url")
        name = p.get("name")
        price = p.get("price")
        discount_text = p.get("discount", "")

        if not url:
            continue

        old_price = previous_prices.get(url)

        # 1. PRICE DROP ALERT
        if old_price and price and price < old_price:
            drop = round(((old_price - price) / old_price) * 100, 2)

            alerts.append({
                "type": "PRICE_DROP",
                "brand": brand_slug,
                "name": name,
                "old_price": old_price,
                "new_price": price,
                "drop_percent": drop,
                "url": url
            })

        # 2. NEW DISCOUNT ALERT (IMPORTANT)
        if discount_text and ("%" in discount_text or "SALE" in discount_text.upper()):
            alerts.append({
                "type": "DISCOUNT_DETECTED",
                "brand": brand_slug,
                "name": name,
                "discount": discount_text,
                "price": price,
                "url": url
            })

        # store latest price
        if price:
            previous_prices[url] = price

    return alerts