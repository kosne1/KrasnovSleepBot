from aiogram.types import InlineKeyboardMarkup

from app.keyboards.buttons import by_alarm_buttons, buttons_back, buttons_start, boolean_buttons, buttons_answer

keyboard_by_alarm_buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=by_alarm_buttons,
                                                                       resize_keyboard=True)
keyboard_buttons_back: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=buttons_back,
                                                                   resize_keyboard=True)

keyboard_start_buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=buttons_start,
                                                                    resize_keyboard=True)

keyboard_boolean_buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=boolean_buttons,
                                                                      resize_keyboard=True)

keyboard_buttons_answer: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=buttons_answer,
                                                                     resize_keyboard=True)
