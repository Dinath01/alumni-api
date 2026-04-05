from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler

from app.db.database import SessionLocal
from app.services.featured_service import select_daily_winner

scheduler = BackgroundScheduler()


def run_daily_winner_selection():
    db = SessionLocal()
    try:
        select_daily_winner(db, date.today())
        print("Daily winner selection executed successfully.")
    except Exception as e:
        print(f"Ran in to an Error during daily winner selection: {e}")
    finally:
        db.close()


def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            run_daily_winner_selection,
            trigger="interval",
            minutes=1,
            id="daily_winner_selection",
            replace_existing=True,
        )
        scheduler.start()