from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

button_start_fill: KeyboardButton = KeyboardButton(text='Заполнить дневник сна')
button_start_help: KeyboardButton = KeyboardButton(text='Написать Саше')
button_start_book: KeyboardButton = KeyboardButton(text='Выбрать книжку')
button_start_donate: KeyboardButton = KeyboardButton(text='Задонатить')

buttons_start: list[KeyboardButton] = [
                                       [button_start_fill, button_start_help],
                                       [button_start_book, button_start_donate]
                                        ]
keyboard_start_buttons: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=buttons_start,
                                    resize_keyboard=True)
