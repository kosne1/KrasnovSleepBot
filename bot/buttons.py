from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup

button_start_fill: KeyboardButton = KeyboardButton(text='Заполнить дневник сна')
button_start_help: KeyboardButton = KeyboardButton(text='Написать Саше')
button_start_book: KeyboardButton = KeyboardButton(text='Выбрать книжку')
button_start_donate: KeyboardButton = KeyboardButton(text='Задонатить')

buttons_start: list[list[KeyboardButton]] = [
    [button_start_fill, button_start_help],
    [button_start_book, button_start_donate]
]
keyboard_start_buttons: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=buttons_start,
                                                                  resize_keyboard=True)
inline_button_yes: InlineKeyboardButton = InlineKeyboardButton(text='Да',
                                                               callback_data='inline_button_yes_press')
inline_button_no: InlineKeyboardButton = InlineKeyboardButton(text='Нет',
                                                              callback_data='inline_button_no_press')
boolean_buttons: list[list[InlineKeyboardButton]] = [[inline_button_yes, inline_button_no]]
keyboard_boolean_buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=boolean_buttons,
                                                                      resize_keyboard=True)
inline_button_yes: InlineKeyboardButton = InlineKeyboardButton(text='Да',
                                                               callback_data='inline_button_yes_press')
inline_button_not_first: InlineKeyboardButton = InlineKeyboardButton(text='Да, но не с первым звонком',
                                                                     callback_data='inline_button_not_first_press')
inline_button_earlier: InlineKeyboardButton = InlineKeyboardButton(text='Нет, раньше будильника',
                                                                  callback_data='inline_button_earlier_press')
inline_button_late: InlineKeyboardButton = InlineKeyboardButton(text='Нет, проспал\проспала',
                                                                callback_data='inline_button_late_pressed')
inline_button_no: InlineKeyboardButton = InlineKeyboardButton(text='Нет',
                                                              callback_data='inline_button_no_press')
by_alarm_buttons: list[list[InlineKeyboardButton]] = [
    [inline_button_yes, inline_button_no],
    [inline_button_not_first],
    [inline_button_earlier],
    [inline_button_late]
]
keyboard_by_alarm_buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=by_alarm_buttons,
                                                                       resize_keyboard=True)

