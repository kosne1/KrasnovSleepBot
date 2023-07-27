from aiogram import executor

from app.commands import *
from app.handlers import *
from app.scheduler import scheduler, check_finished_dairy_notification

if __name__ == '__main__':
    scheduler.add_job(check_finished_dairy_notification, 'interval', minutes=1)
    scheduler.start()
    print('Bot is running...')
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
