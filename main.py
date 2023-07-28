from datetime import datetime

from aiogram import executor
from apscheduler.triggers.cron import CronTrigger

from app.commands import *
from app.handlers import *
from app.scheduler import scheduler, check_finished_dairy_notification

if __name__ == '__main__':
    scheduler.add_job(func=check_finished_dairy_notification,
                      trigger=CronTrigger(hour='0,9,12,20'), run_date=datetime(2023, 7, 28, 11, 55, 0))
    scheduler.start()
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
