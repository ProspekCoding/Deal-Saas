from app.scraper import scrape_products
from app.database import SessionLocal
from app.models import ProductPrice
import asyncio


def check_brand(brand_slug: str):

    session = SessionLocal()

    try:
        products = asyncio.run(scrape_products(brand_slug))
    except:
        return []

    alerts = []

    for p in products:

        if not isinstance(p, dict):
            continue

        name = p.get("name")
        price = p.get("price")

        if price is None:
            continue

        key = name + brand_slug

        last = session.query(ProductPrice)\
            .filter_by(product_key=key)\
            .order_by(ProductPrice.timestamp.desc())\
            .first()

        old_price = last.price if last else None

        # save current snapshot
        session.add(ProductPrice(
            product_key=key,
            brand=brand_slug,
            name=name,
            price=price,
            old_price=old_price
        ))
        session.commit()

        # ALERT LOGIC
        if old_price and price < old_price:

            drop = round(((old_price - price) / old_price) * 100, 2)

            alerts.append({
                "brand": brand_slug,
                "name": name,
                "old_price": old_price,
                "new_price": price,
                "drop_percent": drop
            })

    session.close()
    return alerts