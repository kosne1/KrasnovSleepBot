from aiogram.types import InlineKeyboardButton

button_start_fill: InlineKeyboardButton = InlineKeyboardButton(text='Заполнить дневник сна',
                                                               callback_data='button_start_fill_pressed')
button_start_help: InlineKeyboardButton = InlineKeyboardButton(text='Написать Саше',
                                                               callback_data='button_start_help_pressed')
button_start_book: InlineKeyboardButton = InlineKeyboardButton(text='Выбрать книжку',
                                                               callback_data='button_start_book_pressed')
button_start_donate: InlineKeyboardButton = InlineKeyboardButton(text='Задонатить',
                                                                 callback_data='button_start_donate_pressed')
button_back: InlineKeyboardButton = InlineKeyboardButton(text='Заполнить заново',
                                                         callback_data='button_back_pressed')
button_answer_num_1: InlineKeyboardButton = InlineKeyboardButton(text='1',
                                                                 callback_data='button_answer_num_1_pressed')
button_answer_num_2: InlineKeyboardButton = InlineKeyboardButton(text='2',
                                                                 callback_data='button_answer_num_2_pressed')
button_answer_num_3: InlineKeyboardButton = InlineKeyboardButton(text='3',
                                                                 callback_data='button_answer_num_3_pressed')
button_answer_num_4: InlineKeyboardButton = InlineKeyboardButton(text='4',
                                                                 callback_data='button_answer_num_4_pressed')
button_answer_num_5: InlineKeyboardButton = InlineKeyboardButton(text='5',
                                                                 callback_data='button_answer_num_5_pressed')
button_answer_num_6: InlineKeyboardButton = InlineKeyboardButton(text='6',
                                                                 callback_data='button_answer_num_6_pressed')
button_answer_num_7: InlineKeyboardButton = InlineKeyboardButton(text='7',
                                                                 callback_data='button_answer_num_7_pressed')
button_answer_num_8: InlineKeyboardButton = InlineKeyboardButton(text='8',
                                                                 callback_data='button_answer_num_8_pressed')
button_answer_num_9: InlineKeyboardButton = InlineKeyboardButton(text='9',
                                                                 callback_data='button_answer_num_9_pressed')
button_answer_num_10: InlineKeyboardButton = InlineKeyboardButton(text='10',
                                                                  callback_data='button_answer_num_10_pressed')
inline_button_yes: InlineKeyboardButton = InlineKeyboardButton(text='Да',
                                                               callback_data='inline_button_yes_press')
inline_button_no: InlineKeyboardButton = InlineKeyboardButton(text='Нет',
                                                              callback_data='inline_button_no_press')
inline_button_not_first: InlineKeyboardButton = InlineKeyboardButton(text='Да, но не с первым звонком',
                                                                     callback_data='inline_button_not_first_press')
inline_button_earlier: InlineKeyboardButton = InlineKeyboardButton(text='Нет, раньше будильника',
                                                                   callback_data='inline_button_earlier_press')
inline_button_late: InlineKeyboardButton = InlineKeyboardButton(text='Нет, проспал\проспала',
                                                                callback_data='inline_button_late_pressed')

boolean_buttons: list[list[InlineKeyboardButton]] = [
    [inline_button_yes, inline_button_no],
    [button_back]
]
buttons_start: list[list[InlineKeyboardButton]] = [
    [button_start_fill, button_start_help],
    [button_start_book, button_start_donate]
]
buttons_answer: list[list[InlineKeyboardButton]] = [
    [button_answer_num_1, button_answer_num_2, button_answer_num_3, button_answer_num_4, button_answer_num_5],
    [button_answer_num_6, button_answer_num_7, button_answer_num_8, button_answer_num_9, button_answer_num_10],
    [button_back]
]
buttons_back: list[list[InlineKeyboardButton]] = [
    [button_back]
]
by_alarm_buttons: list[list[InlineKeyboardButton]] = [
    [inline_button_yes, inline_button_no],
    [inline_button_not_first],
    [inline_button_earlier],
    [inline_button_late],
    [button_back]
]


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
    elif callback_data == 'button_answer_num_1_pressed':
        return '1'
    elif callback_data == 'button_answer_num_2_pressed':
        return '2'
    elif callback_data == 'button_answer_num_3_pressed':
        return '3'
    elif callback_data == 'button_answer_num_4_pressed':
        return '4'
    elif callback_data == 'button_answer_num_5_pressed':
        return '5'
    elif callback_data == 'button_answer_num_6_pressed':
        return '6'
    elif callback_data == 'button_answer_num_7_pressed':
        return '7'
    elif callback_data == 'button_answer_num_8_pressed':
        return '8'
    elif callback_data == 'button_answer_num_9_pressed':
        return '9'
    elif callback_data == 'button_answer_num_10_pressed':
        return '10'
