from fastapi import FastAPI
from app.tracker import check_brand
from app.brands import BRANDS
from app.database import Base, engine
from app.scheduler import start_scheduler

app = FastAPI()

Base.metadata.create_all(bind=engine)

start_scheduler()


@app.get("/")
def home():
    return {"status": "Production SaaS Running"}


@app.get("/check/{brand}")
def check(brand: str):

    if brand not in BRANDS:
        return {"error": "Brand not supported"}

    alerts = check_brand(BRANDS[brand])

    return {
        "brand": brand,
        "alerts": alerts
    }


@app.get("/check-all")
def check_all():
    all_alerts = []

    for brand, slug in BRANDS.items():
        alerts = check_brand(slug)
        all_alerts.extend(alerts)

    return {
        "total_alerts": len(all_alerts),
        "alerts": all_alerts
    }