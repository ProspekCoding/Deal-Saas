from app.scraper_zalando import scrape_zalando_products

previous_prices = {}

def check_brand(brand_slug):
    products = scrape_zalando_products(brand_slug)

    alerts = []

    for p in products:
        key = p["url"]

        if not p.get("price"):
            continue

        old_price = previous_prices.get(key)

        if old_price and p["price"] < old_price:
            alerts.append({
                "brand": brand_slug,
                "name": p["name"],
                "old_price": old_price,
                "new_price": p["price"],
                "drop_percent": round(((old_price - p["price"]) / old_price) * 100, 2)
            })

        previous_prices[key] = p["price"]

    return alerts