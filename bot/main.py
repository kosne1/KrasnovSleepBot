import datetime
import time

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from buttons import *
from config import BOT_TOKEN, ADMIN_CHAT_ID

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class FSMFillDiary(StatesGroup):
    fill_quality_sleep = State()
    fill_drowsiness = State()
    fill_mood = State()
    fill_selffeeling_morning = State()
    fill_time_turn_bed = State()
    fill_time_turnoff_ligth = State()
    fill_time_start_sleep_minutes = State()
    fill_how_many_wakingups = State()
    fill_sum_wakingups_time_minutes = State()
    fill_time_final_wakingup = State()
    fill_wakingup_earlier = State()
    fill_wakingup_by_alam = State()
    fill_time_sleeping_night = State()
    fill_time_sleeping_day = State()
    fill_did_sport = State()
    fill_drink_alcohol = State()
    fill_use_hypnotic = State()
    fill_use_narcos = State()
    fill_meditate = State()
    fill_coffein_before_14 = State()
    fill_coffein_after_14 = State()
    fill_use_other_stimulators = State()
    fill_comment = State()


class FSMFillName(StatesGroup):
    name = State()


last_fill_timestamp = {}
all_users: dict = {}


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
    if str(message.from_user.id) not in all_users:
        print(all_users)
        print(message.from_user.id)
        await message.answer('Введите ваше ФИО')
        await FSMFillName.name.set()
        if message.from_user.id in all_users:
            print(all_users[f'{message.from_user.id}'])
    else:
        await message.answer(
            text='''Выберите одну из опций''',
            reply_markup=keyboard_start_buttons)


@dp.message_handler(state=FSMFillName.name)
async def set_name(message: Message, state: FSMContext):
    all_users[f'{message.from_user.id}'] = message.text
    print('в словарь попало имя', all_users[f'{message.from_user.id}'])
    await message.answer('Выберите одну из опций',
                         reply_markup=keyboard_start_buttons)
    print(all_users[f'{message.from_user.id}'])
    print('лог id от выбора опций', message.from_user.id)
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()


@dp.callback_query_handler(Text(['button_back_pressed']), state='*')
async def button_back_pressed(callback: CallbackQuery):
    await callback.message.answer(
        text='''Добро пожаловать в бот Dreamy, придуманный @sasha_krasnow для помощи при бессоннице!''',
        reply_markup=keyboard_start_buttons)


def check_notification():
    notification_hours = [9, 12, 20]
    current_hour = datetime.datetime.today().hour
    today_timestamp = int(
        datetime.datetime.today().timestamp()) - datetime.datetime.today().hour * 3600 - datetime.datetime.today().minute * 60

    if current_hour in notification_hours:
        for id in last_fill_timestamp:
            if last_fill_timestamp[id] < today_timestamp:
                bot.send_message(chat_id=id, text='Пожалуйста, заполните дневник сна')


scheduler = AsyncIOScheduler()
scheduler.add_job(check_notification, 'interval', minutes=60)
scheduler.start()


@dp.callback_query_handler(Text(['button_start_fill_pressed']), state='*')
async def start_filling_diary(callback: CallbackQuery):
    today_timestamp = int(
        datetime.datetime.today().timestamp()) - datetime.datetime.today().hour * 3600 - datetime.datetime.today().minute * 60
    print(callback.from_user, 108)
    print('текущий словарь', all_users)
    print('логирую user.id', str(callback.from_user.id))
    if str(callback.from_user.id) in last_fill_timestamp:
        print('второй лог', time.time())
        if today_timestamp < int(last_fill_timestamp[str(callback.from_user.id)]):
            await callback.answer(  # здесь происходит ебейший калбек.ансуэр
                text='''Вы уже заполнили дневник сна. Попробуйте заполнить дневник снова завтра.''')
            return
    print(last_fill_timestamp)
    await FSMFillDiary.fill_quality_sleep.set()
    await callback.message.answer(text='Как вы оцениваете своё сегодняшнее качество сна?',
                                  reply_markup=keyboard_buttons_answer)


@dp.callback_query_handler(Text(['button_start_help_pressed']), state='*')
async def write_to_sasha(callback: CallbackQuery):
    await callback.message.answer(text='https://t.me/sasha_krasnow')


@dp.callback_query_handler(Text(['button_start_book_pressed']), state='*')
async def write_to_sasha(callback: CallbackQuery):
    await callback.message.answer(text='https://t.me/krasnov_books/13')


@dp.callback_query_handler(Text(['button_start_donate_pressed']), state='*')
async def write_to_sasha(callback: CallbackQuery):
    await callback.message.answer(text='2202202317987984')


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Заполнение дневника отменено', reply_markup=keyboard_start_buttons)


@dp.callback_query_handler(lambda query: query.data.startswith('button_answer_num_'),
                           state=FSMFillDiary.fill_quality_sleep)
async def process_turn_to_next_step(query: CallbackQuery, state: FSMContext):
    callback_id = query.data.split('_')[3]
    if callback_id == 1:
        await state.update_data(fill_quality_sleep=callback_data_to_text(str(query.data)))
    elif callback_id == 2:
        await state.update_data(fill_quality_sleep=callback_data_to_text(str(query.data)))
    elif callback_id == 3:
        await state.update_data(fill_quality_sleep=callback_data_to_text(str(query.data)))
    elif callback_id == 4:
        await state.update_data(fill_quality_sleep=callback_data_to_text(str(query.data)))
    elif callback_id == 5:
        await state.update_data(fill_quality_sleep=callback_data_to_text(str(query.data)))
    elif callback_id == 6:
        await state.update_data(fill_quality_sleep=callback_data_to_text(str(query.data)))
    elif callback_id == 7:
        await state.update_data(fill_quality_sleep=callback_data_to_text(str(query.data)))
    elif callback_id == 8:
        await state.update_data(fill_quality_sleep=callback_data_to_text(str(query.data)))
    elif callback_id == 9:
        await state.update_data(fill_quality_sleep=callback_data_to_text(str(query.data)))
    else:
        await state.update_data(fill_quality_sleep=callback_data_to_text(str(query.data)))
    await query.message.answer('Как вы оцениваете свою сонливость вчера в течение дня?',
                               reply_markup=keyboard_buttons_answer)
    await FSMFillDiary.next()


@dp.callback_query_handler(lambda query: query.data.startswith('button_answer_num_'),
                           state=FSMFillDiary.fill_drowsiness)
async def process_turn_to_next_step(query: CallbackQuery, state: FSMContext):
    callback_id = query.data.split('_')[3]
    if callback_id == 1:
        await state.update_data(fill_drowsiness=callback_data_to_text(str(query.data)))
    elif callback_id == 2:
        await state.update_data(fill_drowsiness=callback_data_to_text(str(query.data)))
    elif callback_id == 3:
        await state.update_data(fill_drowsiness=callback_data_to_text(str(query.data)))
    elif callback_id == 4:
        await state.update_data(fill_drowsiness=callback_data_to_text(str(query.data)))
    elif callback_id == 5:
        await state.update_data(fill_drowsiness=callback_data_to_text(str(query.data)))
    elif callback_id == 6:
        await state.update_data(fill_drowsiness=callback_data_to_text(str(query.data)))
    elif callback_id == 7:
        await state.update_data(fill_drowsiness=callback_data_to_text(str(query.data)))
    elif callback_id == 8:
        await state.update_data(fill_drowsiness=callback_data_to_text(str(query.data)))
    elif callback_id == 9:
        await state.update_data(fill_drowsiness=callback_data_to_text(str(query.data)))
    else:
        await state.update_data(fill_drowsiness=callback_data_to_text(str(query.data)))
    await query.message.answer('Как вы оцениваете своё настроение вчера в течение дня?',
                               reply_markup=keyboard_buttons_answer)
    await FSMFillDiary.next()


@dp.callback_query_handler(lambda query: query.data.startswith('button_answer_num_'),
                           state=FSMFillDiary.fill_mood)
async def process_turn_to_next_step(query: CallbackQuery, state: FSMContext):
    callback_id = query.data.split('_')[3]
    if callback_id == 1:
        await state.update_data(fill_mood=callback_data_to_text(str(query.data)))
    elif callback_id == 2:
        await state.update_data(fill_mood=callback_data_to_text(str(query.data)))
    elif callback_id == 3:
        await state.update_data(fill_mood=callback_data_to_text(str(query.data)))
    elif callback_id == 4:
        await state.update_data(fill_mood=callback_data_to_text(str(query.data)))
    elif callback_id == 5:
        await state.update_data(fill_mood=callback_data_to_text(str(query.data)))
    elif callback_id == 6:
        await state.update_data(fill_mood=callback_data_to_text(str(query.data)))
    elif callback_id == 7:
        await state.update_data(fill_mood=callback_data_to_text(str(query.data)))
    elif callback_id == 8:
        await state.update_data(fill_mood=callback_data_to_text(str(query.data)))
    elif callback_id == 9:
        await state.update_data(fill_mood=callback_data_to_text(str(query.data)))
    else:
        await state.update_data(fill_mood=callback_data_to_text(str(query.data)))
    await FSMFillDiary.next()
    await query.message.answer('Как вы оцениваете своё состояние (бодрость, активность) наутро?',
                               reply_markup=keyboard_buttons_answer)


@dp.callback_query_handler(lambda query: query.data.startswith('button_answer_num_'),
                           state=FSMFillDiary.fill_selffeeling_morning)
async def process_turn_to_next_step(query: CallbackQuery, state: FSMContext):
    callback_id = query.data.split('_')[3]
    if callback_id == 1:
        await state.update_data(fill_selffeeling_morning=callback_data_to_text(str(query.data)))
    elif callback_id == 2:
        await state.update_data(fill_selffeeling_morning=callback_data_to_text(str(query.data)))
    elif callback_id == 3:
        await state.update_data(fill_selffeeling_morning=callback_data_to_text(str(query.data)))
    elif callback_id == 4:
        await state.update_data(fill_selffeeling_morning=callback_data_to_text(str(query.data)))
    elif callback_id == 5:
        await state.update_data(fill_selffeeling_morning=callback_data_to_text(str(query.data)))
    elif callback_id == 6:
        await state.update_data(fill_selffeeling_morning=callback_data_to_text(str(query.data)))
    elif callback_id == 7:
        await state.update_data(fill_selffeeling_morning=callback_data_to_text(str(query.data)))
    elif callback_id == 8:
        await state.update_data(fill_selffeeling_morning=callback_data_to_text(str(query.data)))
    elif callback_id == 9:
        await state.update_data(fill_selffeeling_morning=callback_data_to_text(str(query.data)))
    else:
        await state.update_data(fill_selffeeling_morning=callback_data_to_text(str(query.data)))
    await FSMFillDiary.next()
    await query.message.answer('Во сколько вы вчера легли в кровать?(В ответ напишите время в формате 00:00)',
                               reply_markup=keyboard_buttons_back)


@dp.message_handler(
    lambda message: not len(message.text) == 5 or not message.text[2] == ':' or not message.text.split(':')[
        0].isdigit() or not message.text.split(':')[1].isdigit(),
    state=FSMFillDiary.fill_time_turn_bed)
async def process_answer_24_format_invalid(message: types.Message):
    return await message.reply("В ответ введите время в 24-х часовом формате, например 00:00",
                               reply_markup=keyboard_buttons_back)


@dp.message_handler(
    lambda message: 0 <= int(message.text.split(':')[0]) <= 23 and 0 <= int(message.text.split(':')[1]) <= 59,
    state=FSMFillDiary.fill_time_turn_bed)
async def process_turn_to_next_step(message: types.Message, state: FSMContext):
    await state.update_data(fill_time_turn_bed=str(message.text))
    await message.answer('Во сколько вы выключили свет и решили заснуть?(В ответ напишите время в формате 00:00)',
                         reply_markup=keyboard_buttons_back)
    await FSMFillDiary.next()


@dp.message_handler(
    lambda message: not len(message.text) == 5 or not message.text[2] == ':' or not message.text.split(':')[
        0].isdigit() or not message.text.split(':')[1].isdigit(),
    state=FSMFillDiary.fill_time_turnoff_ligth)
async def process_answer_24_format_invalid(message: types.Message):
    return await message.reply("В ответ введите время в 24-х часовом формате, например 00:00",
                               reply_markup=keyboard_buttons_back)


@dp.message_handler(
    lambda message: 0 <= int(message.text.split(':')[0]) <= 23 and 0 <= int(message.text.split(':')[1]) <= 59,
    state=FSMFillDiary.fill_time_turnoff_ligth)
async def process_turn_to_next_step(message: types.Message, state: FSMContext):
    await state.update_data(fill_time_turnoff_ligth=str(message.text))
    await message.answer('Сколько примерно у вас ушло времени, чтобы заснуть (в минутах)?',
                         reply_markup=keyboard_buttons_back)
    await FSMFillDiary.next()


@dp.message_handler(lambda message: not message.text.isdigit(),
                    state=FSMFillDiary.fill_time_start_sleep_minutes)
async def process_answer_1_10_invalid(message: types.Message):
    return await message.reply("В ответ введите число минут")


@dp.message_handler(lambda message: message.text.isdigit(), state=FSMFillDiary.fill_time_start_sleep_minutes)
async def process_turn_to_next_step(message: types.Message, state: FSMContext):
    await state.update_data(fill_time_start_sleep_minutes=int(message.text))
    await message.answer('Сколько раз вы просыпались среди ночи (до окончательного утреннего пробуждения)?',
                         reply_markup=keyboard_buttons_back)
    await FSMFillDiary.next()


@dp.message_handler(lambda message: message.text.isdigit(), state=FSMFillDiary.fill_how_many_wakingups)
async def process_turn_to_next_step(message: types.Message, state: FSMContext):
    await state.update_data(fill_how_many_wakingups=str(message.text))
    await message.answer('Сколько времени суммарно длились эти пробуждения? (в минутах)',
                         reply_markup=keyboard_buttons_back)
    await FSMFillDiary.next()


@dp.message_handler(lambda message: not message.text.isdigit(),
                    state=FSMFillDiary.fill_sum_wakingups_time_minutes)
async def process_answer_1_10_invalid(message: types.Message):
    return await message.reply("В ответ введите число минут",
                               reply_markup=keyboard_buttons_back)


@dp.message_handler(lambda message: message.text.isdigit(), state=FSMFillDiary.fill_sum_wakingups_time_minutes)
async def process_turn_to_next_step(message: types.Message, state: FSMContext):
    await state.update_data(fill_sum_wakingups_time_minutes=int(message.text))
    await message.answer('Во сколько было ваше финальное пробуждение?(В ответ напишите время в формате 00:00)',
                         reply_markup=keyboard_buttons_back)
    await FSMFillDiary.next()


@dp.message_handler(
    lambda message: not len(message.text) == 5 or not message.text[2] == ':' or not message.text.split(':')[
        0].isdigit() or not message.text.split(':')[1].isdigit(),
    state=FSMFillDiary.fill_time_final_wakingup)
async def process_answer_24_format_invalid(message: Message):
    return await message.reply("В ответ введите время в 24-х часовом формате, например 00:00")


@dp.message_handler(
    lambda message: 0 <= int(message.text.split(':')[0]) <= 23 and 0 <= int(message.text.split(':')[1]) <= 59,
    state=FSMFillDiary.fill_time_final_wakingup)
async def process_turn_to_next_step(message: Message, state: FSMContext):
    await state.update_data(fill_time_final_wakingup=str(message.text))
    await message.answer(text='Вы проснулись раньше, чем планировалось?',
                         reply_markup=keyboard_boolean_buttons)
    await FSMFillDiary.next()


@dp.callback_query_handler(state=FSMFillDiary.fill_wakingup_earlier)
async def process_button_boolean_pressed(callback: CallbackQuery, state: FSMContext):
    await state.update_data(fill_wakingup_earlier=callback_data_to_text(str(callback.data)))
    await bot.send_message(callback.message.chat.id,
                           text='Вы проснулись по будильнику?',
                           reply_markup=keyboard_by_alarm_buttons)
    await FSMFillDiary.next()


@dp.callback_query_handler(state=FSMFillDiary.fill_wakingup_by_alam)
async def process_button_boolean_pressed(callback: CallbackQuery, state: FSMContext):
    await state.update_data(fill_wakingup_by_alam=callback_data_to_text(str(callback.data)))
    await bot.send_message(callback.message.chat.id,
                           text='Сколько времени за прошедшую ночь вы спали (по ощущениям в формате 00:00)?')
    await FSMFillDiary.next()


@dp.message_handler(
    lambda message: not len(message.text) == 5 or not message.text[2] == ':' or not message.text.split(':')[
        0].isdigit() or not message.text.split(':')[1].isdigit(),
    state=FSMFillDiary.fill_time_sleeping_night)
async def process_answer_24_format_invalid(message: Message):
    return await message.reply("В ответ введите время в 24-х часовом формате, например 00:00")


@dp.message_handler(
    lambda message: 0 <= int(message.text.split(':')[0]) <= 23 and 0 <= int(message.text.split(':')[1]) <= 59,
    state=FSMFillDiary.fill_time_sleeping_night)
async def process_turn_to_next_step(message: Message, state: FSMContext):
    await state.update_data(fill_time_sleeping_night=str(message.text))
    await message.answer(text='Сколько времени вы спали вчера днём, в формате 00:00?')
    await FSMFillDiary.next()


@dp.message_handler(
    lambda message: not len(message.text) == 5 or not message.text[2] == ':' or not message.text.split(':')[
        0].isdigit() or not message.text.split(':')[1].isdigit(),
    state=FSMFillDiary.fill_time_sleeping_day)
async def process_answer_24_format_invalid(message: Message):
    return await message.reply("В ответ введите время в 24-х часовом формате, например 00:00")


@dp.message_handler(
    lambda message: 0 <= int(message.text.split(':')[0]) <= 23 and 0 <= int(message.text.split(':')[1]) <= 59,
    state=FSMFillDiary.fill_time_sleeping_day)
async def process_turn_to_next_step(message: Message, state: FSMContext):
    await state.update_data(fill_time_sleeping_day=str(message.text))
    await message.answer(text='Занимались ли вы вчера спортом?',
                         reply_markup=keyboard_boolean_buttons)
    await FSMFillDiary.next()


@dp.callback_query_handler(state=FSMFillDiary.fill_did_sport)
async def process_button_boolean_pressed(callback: CallbackQuery, state: FSMContext):
    await state.update_data(fill_did_sport=callback_data_to_text(str(callback.data)))
    await bot.send_message(callback.message.chat.id,
                           text='Пили ли вы вчера алкоголь?',
                           reply_markup=keyboard_boolean_buttons)
    await FSMFillDiary.next()


@dp.callback_query_handler(state=FSMFillDiary.fill_drink_alcohol)
async def process_button_boolean_pressed(callback: CallbackQuery, state: FSMContext):
    await state.update_data(fill_drink_alcohol=callback_data_to_text(str(callback.data)))
    await bot.send_message(callback.message.chat.id,
                           text='Приходилось ли вчера использовать снотворные, включая мелатонин?',
                           reply_markup=keyboard_boolean_buttons)
    await FSMFillDiary.next()


@dp.callback_query_handler(state=FSMFillDiary.fill_use_hypnotic)
async def process_button_boolean_pressed(callback: CallbackQuery, state: FSMContext):
    await state.update_data(fill_use_hypnotic=callback_data_to_text(str(callback.data)))
    await bot.send_message(callback.message.chat.id,
                           text='Курили ли вы вчера марихуану или употребляли CBD?',
                           reply_markup=keyboard_boolean_buttons)
    await FSMFillDiary.next()


@dp.callback_query_handler(state=FSMFillDiary.fill_use_narcos)
async def process_button_boolean_pressed(callback: CallbackQuery, state: FSMContext):
    await state.update_data(fill_use_narcos=callback_data_to_text(str(callback.data)))
    await bot.send_message(callback.message.chat.id,
                           text='Занимались ли вы вчера в течение дня медитацией\дыхательными\другими релаксационными практиками?',
                           reply_markup=keyboard_boolean_buttons)
    await FSMFillDiary.next()


@dp.callback_query_handler(state=FSMFillDiary.fill_meditate)
async def process_button_boolean_pressed(callback: CallbackQuery, state: FSMContext):
    await state.update_data(fill_meditate=callback_data_to_text(str(callback.data)))
    await bot.send_message(callback.message.chat.id,
                           text='Пили ли Вы вчера напитки с кофеином до 14 часов дня?',
                           reply_markup=keyboard_boolean_buttons)
    await FSMFillDiary.next()


@dp.callback_query_handler(state=FSMFillDiary.fill_coffein_before_14)
async def process_button_boolean_pressed(callback: CallbackQuery, state: FSMContext):
    await state.update_data(fill_coffein_before_14=callback_data_to_text(str(callback.data)))
    await bot.send_message(callback.message.chat.id,
                           text='Пили ли Вы вчера напитки с кофеином после 14 часов дня?',
                           reply_markup=keyboard_boolean_buttons)
    await FSMFillDiary.next()


@dp.callback_query_handler(state=FSMFillDiary.fill_coffein_after_14)
async def process_button_boolean_pressed(callback: CallbackQuery, state: FSMContext):
    await state.update_data(fill_coffein_after_14=callback_data_to_text(str(callback.data)))
    await bot.send_message(callback.message.chat.id,
                           text='Принимали ли Вы другие стимуляторы?',
                           reply_markup=keyboard_boolean_buttons)
    await FSMFillDiary.next()


@dp.callback_query_handler(state=FSMFillDiary.fill_use_other_stimulators)
async def process_button_boolean_pressed(callback: CallbackQuery, state: FSMContext):
    await state.update_data(fill_use_other_stimulators=callback_data_to_text(str(callback.data)))
    await bot.send_message(callback.message.chat.id,
                           text='Оставить комментарий (факторы, которые могли повлиять на сон):')
    await FSMFillDiary.next()


@dp.message_handler(state=FSMFillDiary.fill_comment)
async def process_turn_to_next_step(message: types.Message, state: FSMContext):
    await state.update_data(fill_comment=str(message.text))
    await message.answer('Спасибо за заполнение дневника',
                         reply_markup=keyboard_start_buttons)
    session = storage.data[str(message.chat.id)][str(message.chat.id)]['data']
    print(session)
    await bot.send_message(ADMIN_CHAT_ID,
                           text=f'''Дневник сна заполнен пользователем по имени {all_users[f'{message.from_user.id}']}, юзернейм: @{message.from_user.username}\n------
1) Как вы оцениваете своё сегодняшнее качество сна? (здесь и далее: 10 – высшая оценка)\n------\n{session['fill_quality_sleep']}\n------
2) Как вы оцениваете свою сонливость вчера в течение дня?\n------\n{session['fill_drowsiness']}\n------
3) Как вы оцениваете своё настроение вчера в течение дня?\n------\n{session['fill_mood']}\n------
4) Как вы оцениваете своё состояние (бодрость, активность) наутро?\n------\n{session['fill_selffeeling_morning']}\n------
5) Во сколько вы вчера легли в кровать?\n------\n{session['fill_time_turn_bed']}\n------
6) Во сколько вы выключили свет и решили заснуть?\n------\n{session['fill_time_turnoff_ligth']}\n------
7) Сколько примерно у вас ушло времени, чтобы заснуть (в минутах)?\n------\n{session['fill_time_start_sleep_minutes']}\n------
8) Сколько раз вы просыпались среди ночи (до окончательного утреннего пробуждения)?\n------\n{session['fill_how_many_wakingups']}\n------
9) Сколько времени примерно суммарно длились эти пробуждения (в минутах)?\n------\n{session['fill_sum_wakingups_time_minutes']}\n------
10) Во сколько было ваше финальное пробуждение?\n------\n{session['fill_time_final_wakingup']}\n------
11) Вы проснулись раньше, чем планировалось?\n------\n{session['fill_wakingup_earlier']}\n------
12) Вы проснулись по будильнику?\n------\n{session['fill_wakingup_by_alam']}\n------
13) Сколько времени за прошедшую ночь вы спали (по ощущениям)?\n------\n{session['fill_time_sleeping_night']}\n------
14) Сколько времени вы спали вчера днём?\n------\n{session['fill_time_sleeping_day']}\n------
15) Занимались ли вы вчера спортом?\n------\n{session['fill_did_sport']}\n------
16) Пили ли вы вчера алкоголь?\n------\n{session['fill_drink_alcohol']}\n------\n------\n{session['fill_did_sport']}\n------
17) Приходилось ли вчера использовать снотворные, включая мелатонин?\n------\n{session['fill_use_hypnotic']}\n------
18) Курили ли вы вчера марихуану или употребляли CBD?\n------\n{session['fill_use_narcos']}\n------
19) Занимались ли вы вчера в течение дня медитацией\дыхательными\ другими релаксационными практиками?\n------\n{session['fill_meditate']}\n------
20) Пили ли Вы вчера напитки с кофеином до 14 часов дня?\n------\n{session['fill_coffein_before_14']}\n------
21) Пили ли Вы вчера напитки с кофеином после 14 часов дня?\n------\n{session['fill_coffein_after_14']}\n------
22) Принимали ли Вы другие стимуляторы?\n------\n{session['fill_use_other_stimulators']}\n------
23) Оставить комментарий (факторы, которые могли повлиять на сон):\n------\n{session['fill_comment']}\n------''')

    last_fill_timestamp[str(message.from_user.id)] = int(datetime.datetime.now().timestamp())

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    print(last_fill_timestamp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
