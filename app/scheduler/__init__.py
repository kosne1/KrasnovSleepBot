import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app import bot
from app.configs import notification_hours
from app.keyboards import keyboard_start_buttons
from app.services import user_service, JsonService


async def check_finished_dairy_notification() -> None:
    log_file = open("error.log", "w")
    current_hour = datetime.datetime.today().hour
    users = user_service.get_users()
    if current_hour == 1:
        JsonService().update_is_finished_diary_to_false()
        return
    for user in users:
        try:
            if not user.is_finished_diary_today and current_hour in notification_hours:
                await bot.send_message(chat_id=user.chat_id, text='Пожалуйста, заполните дневник сна!',
                                       reply_markup=keyboard_start_buttons)
        except Exception as e:
            log_file.write(f"[ERROR {datetime.datetime.now()}]: {str(user)}, {str(e)}")


scheduler = AsyncIOScheduler()
