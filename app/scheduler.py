from apscheduler.schedulers.background import BackgroundScheduler
from app.tracker import check_brand
from app.brands import BRANDS


scheduler = BackgroundScheduler()


def run_tracking_job():
    print("Running scheduled tracking job...")

    for brand, slug in BRANDS.items():
        alerts = check_brand(slug)

        if alerts:
            print(f"[ALERT] {brand}: {len(alerts)} deals found")


def start_scheduler():
    scheduler.add_job(run_tracking_job, "interval", minutes=10)
    scheduler.start()