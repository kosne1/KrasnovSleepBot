from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup

button_start_fill: InlineKeyboardButton = InlineKeyboardButton(text='Заполнить дневник сна',
                                                               callback_data='button_start_fill_pressed')
button_start_help: InlineKeyboardButton = InlineKeyboardButton(text='Написать Саше',
                                                               callback_data='button_start_help_pressed')
button_start_book: InlineKeyboardButton = InlineKeyboardButton(text='Выбрать книжку',
                                                               callback_data='button_start_book_pressed')
button_start_donate: InlineKeyboardButton = InlineKeyboardButton(text='Задонатить',
                                                                 callback_data='button_start_donate_pressed')
button_back: InlineKeyboardButton = InlineKeyboardButton(text='Назад',
                                                         callback_data='button_back_pressed')

buttons_start: list[list[InlineKeyboardButton]] = [
    [button_start_fill, button_start_help],
    [button_start_book, button_start_donate]
]
buttons_back: list[list[InlineKeyboardButton]] = [
    [button_back]
]
keyboard_buttons_back: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=buttons_back,
                                                                   resize_keyboard=True)

keyboard_start_buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=buttons_start,
                                                                    resize_keyboard=True)

inline_button_yes: InlineKeyboardButton = InlineKeyboardButton(text='Да',
                                                               callback_data='inline_button_yes_press')
inline_button_no: InlineKeyboardButton = InlineKeyboardButton(text='Нет',
                                                              callback_data='inline_button_no_press')

boolean_buttons: list[list[InlineKeyboardButton]] = [
    [inline_button_yes, inline_button_no],
    [button_back]
]

keyboard_boolean_buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=boolean_buttons,
                                                                      resize_keyboard=True)

inline_button_not_first: InlineKeyboardButton = InlineKeyboardButton(text='Да, но не с первым звонком',
                                                                     callback_data='inline_button_not_first_press')
inline_button_earlier: InlineKeyboardButton = InlineKeyboardButton(text='Нет, раньше будильника',
                                                                   callback_data='inline_button_earlier_press')
inline_button_late: InlineKeyboardButton = InlineKeyboardButton(text='Нет, проспал\проспала',
                                                                callback_data='inline_button_late_pressed')

by_alarm_buttons: list[list[InlineKeyboardButton]] = [
    [inline_button_yes, inline_button_no],
    [inline_button_not_first],
    [inline_button_earlier],
    [inline_button_late],
    [button_back]
]
keyboard_by_alarm_buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=by_alarm_buttons,
                                                                       resize_keyboard=True)


def callback_data_to_text(callback_data: str) -> str:
    if callback_data == 'inline_button_yes_press':
        return 'Да'
    elif callback_data == 'inline_button_no_press':
        return 'Нет'
    elif callback_data == 'inline_button_not_first_press':
        return 'Да, но не с первым звонком'
    elif callback_data == 'inline_button_earlier_press':
        return 'Нет, раньше будильника'
    elif callback_data == 'inline_button_late_pressed':
        return 'Нет, проспал\проспала'
