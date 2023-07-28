import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app import bot
from app.configs import notification_hours
from app.keyboards import keyboard_start_buttons
from app.services import user_service


async def check_finished_dairy_notification() -> None:
    current_hour = datetime.datetime.today().hour
    users = user_service.get_users()
    for user in users:
        if current_hour == 0:
            user = user.is_finished_diary_today = False
            user_service.upsert_user(user)
            return
        if not user.is_finished_diary_today and current_hour in notification_hours:
            await bot.send_message(chat_id=user.chat_id, text='Пожалуйста, заполните дневник сна!',
                                   reply_markup=keyboard_start_buttons)

scheduler = AsyncIOScheduler()
