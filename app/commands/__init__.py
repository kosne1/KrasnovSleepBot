from aiogram import types
from aiogram.types import BotCommand

from app.keyboards import keyboard_start_buttons
from app.services import user_service
from app.states import FSMFillName
from main import dp


async def on_startup(_dp):
    user_commands = [
        BotCommand("start", "Старт"),
        BotCommand("cancel", "Отменить заполнение дневника")
    ]
    await _dp.bot.set_my_commands(user_commands)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(
        text='''Добро пожаловать в бот Dreamy, придуманный @sasha_krasnow для помощи при бессоннице!''')
    if user_service.get_user_by_id(message.from_user.id) is None:
        await message.answer('Введите ваше ФИО')
        await FSMFillName.name.set()
    else:
        await message.answer(
            text='''Выберите одну из опций''',
            reply_markup=keyboard_start_buttons)
