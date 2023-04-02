from apscheduler.schedulers.background import BackgroundScheduler
from tasks_manager.scheduler import delete_old_data

scheduler = BackgroundScheduler()
scheduler.add_job(delete_old_data, 'interval', hours=24)
scheduler.start()

