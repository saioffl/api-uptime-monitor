import time

from apscheduler.schedulers.background import BackgroundScheduler
from ..database import SessionLocal
from ..models.monitor import MonitorModel
# from ..schemas.monitor import MonitorBase


def check_website(monitor_id):
    print(f"Checking Website for Monitor {monitor_id}")


def compare_db():
    db = SessionLocal()
    try:
        resp = (
            db.query(MonitorModel.id, MonitorModel.interval_seconds)
            .filter(MonitorModel.is_active.is_(True))
            .all()
        )
        seen_dict_db = {}
        for monitor in resp:
            seen_dict_db[monitor.id] = monitor.interval_seconds
        return seen_dict_db
    finally:
        db.close()


def get_scheduler_ids():
    seen_sch = set()
    jobs = scheduler.get_jobs()
    for job in jobs:
        if job.id.startswith("monitor_"):
            seen_sch.add(int(job.id.replace("monitor_", "")))
    return seen_sch


def sync_monitors():
    # database_monitor has the dictionary for db_ids and db_interval time
    database_monitor = compare_db()
    for key, val in database_monitor.items():
        print(f"DataBase Monitor Info : {key, val}")

    # sch_ids is a set having scheduler ids (which is returning a set)
    sch_ids = get_scheduler_ids()

    # Converting the dictionary of database_monitor to just keys and store them in `db_ids`
    db_ids = set(database_monitor.keys())

    # Comparing new monitor by subracting db_ids with sch_ids, it means some id from db isnt there in scheduler !
    new_monitors = db_ids - sch_ids
    print(f"Exists in MySQL but missing from scheduler: {new_monitors}")

    # Comparing removed_monitors by subracting sch_ids with db_ids, means scheduler has extra id while db dosent have it ! (removed prolly !!)
    removed_monitors = sch_ids - db_ids
    print(f"Exists in Scheduler but missing from MySQL: {removed_monitors}")

    #     # Display Monitors !
    #     for monitor in database_monitor:
    #         print(f"Monitor id : {monitor}")
    #         print(f"Monitor interval : {database_monitor[monitor]}")

    # Add a Monitor !
    for monitor_id in new_monitors:
        scheduler.add_job(
            func=check_website,
            trigger="interval",
            seconds=database_monitor[monitor_id],
            args=[monitor_id],
            id=f"monitor_{monitor_id}",
        )

    # Remove Monitor !
    for monitor_id in removed_monitors:
        scheduler.remove_job(f"monitor_{monitor_id}")
        print(f"Removed Monitor {monitor_id}")

    # Update existing monitors
    existing_monitors = db_ids & sch_ids

    for monitor_id in existing_monitors:
        job_id = f"monitor_{monitor_id}"
        current_job = scheduler.get_job(job_id)
        if current_job is None:
            continue
        current_interval = current_job.trigger.interval.total_seconds()

        database_interval = database_monitor[monitor_id]

        if current_interval != database_interval:
            scheduler.reschedule_job(
                job_id,
                trigger="interval",
                seconds=database_interval,
            )
            print(f"Updated Monitor {monitor_id}")


print("Synchronisation completed!")

scheduler = BackgroundScheduler()

sync_monitors()

scheduler.add_job(
    func=sync_monitors,
    trigger="interval",
    seconds=60,
    id="sync_monitors",
)
scheduler.start()
print("Scheduler started!")

try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
print("Scheduler stopped!")
