from apscheduler.schedulers.background import BackgroundScheduler
from .send_email import appointments_email


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(appointments_email, 'interval', minutes=30)
    scheduler.start()