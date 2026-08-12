from apscheduler.schedulers.background import BackgroundScheduler

from app.database import SessionLocal
from app.services import create_backup


# =====================================================
# Automatic Backup Job
# =====================================================

def automatic_backup():

    db = SessionLocal()

    try:
        result = create_backup(db)

        print(
            f"[AUTO BACKUP] "
            f"Backup created successfully: {result}"
        )

    except Exception as e:

        print(
            f"[AUTO BACKUP ERROR] {e}"
        )

    finally:
        db.close()


# =====================================================
# Scheduler
# =====================================================

scheduler = BackgroundScheduler()


def start_scheduler():

    scheduler.add_job(
        automatic_backup,
        "interval",
        minutes=5,
        id="automatic_backup",
        replace_existing=True
    )

    scheduler.start()

    print(
        "[SCHEDULER] Automatic backup scheduler started."
    )


def stop_scheduler():

    if scheduler.running:
        scheduler.shutdown()

        print(
            "[SCHEDULER] Automatic backup scheduler stopped."
        )