# from prisma import PrismaClient
import datetime
import time

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from buttons import *
from config import BOT_TOKEN

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
    last_fill_timestap = State()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(
        text='''Добро пожаловать в бот Dreamy, придуманный @sasha_krasnow для помощи при бессоннице!\n\nВыберите одну из опций''',
        reply_markup=keyboard_start_buttons)

    @dp.message_handler(Text('Заполнить дневник сна'))
    async def start_filling_diary(message: Message):
        print(storage.data)
        session = storage.data[str(message.chat.id)][str(message.chat.id)]['data']
        if 'last_fill_timestap' in session:
            if int(datetime.datetime.today().timestamp()) < int(session['last_fill_timestap']):
                await message.answer(
                    text='''Вы уже заполнили дневник сна. Попробуйте заполнить дневник снова завтра.''',
                    reply_markup=keyboard_start_buttons)
                return

        await FSMFillDiary.fill_quality_sleep.set()
        await message.answer(text='Как вы оцениваете своё сегодняшнее качество сна от 1 до 10 ?',
                             reply_markup=ReplyKeyboardRemove())
        print(session)

    @dp.message_handler(state='*', commands='cancel')
    @dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
    async def cancel_handler(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return

        await state.finish()
        # And remove keyboard (just in case)
        await message.reply('Заполнение дневника отменено', reply_markup=keyboard_start_buttons)

    @dp.message_handler(lambda message: not message.text.isdigit() or int(message.text) < 0 or int(message.text) > 10,
                        state=FSMFillDiary.fill_quality_sleep)
    async def process_answer_1_10_invalid(message: types.Message):
        return await message.reply("В ответ введите число от 1 до 10")

    @dp.message_handler(lambda message: message.text.isdigit(), state=FSMFillDiary.fill_quality_sleep)
    async def process_turn_to_next_step(message: types.Message, state: FSMContext):
        await state.update_data(fill_quality_sleep=int(message.text))
        await message.answer('Как вы оцениваете свою сонливость вчера в течение дня по шкале от 1 до 10?')
        await FSMFillDiary.next()

    @dp.message_handler(lambda message: not message.text.isdigit() or int(message.text) < 0 or int(message.text) > 10,
                        state=FSMFillDiary.fill_drowsiness)
    async def process_answer_1_10_invalid(message: types.Message):
        return await message.reply("В ответ введите число от 1 до 10")

    @dp.message_handler(lambda message: message.text.isdigit(), state=FSMFillDiary.fill_drowsiness)
    async def process_turn_to_next_step(message: types.Message, state: FSMContext):
        await state.update_data(fill_drowsiness=int(message.text))
        await storage.update_data(chat=message.chat.id, fill_drowsiness=int(message.text))
        await message.answer('Как вы оцениваете своё настроение вчера в течение дня по шкале от 1 до 10?')
        await FSMFillDiary.next()

    @dp.message_handler(lambda message: not message.text.isdigit() or int(message.text) < 0 or int(message.text) > 10,
                        state=FSMFillDiary.fill_mood)
    async def process_answer_1_10_invalid(message: types.Message):
        return await message.reply("В ответ введите число от 1 до 10")

    @dp.message_handler(lambda message: message.text.isdigit(), state=FSMFillDiary.fill_mood)
    async def process_turn_to_next_step(message: types.Message, state: FSMContext):
        await state.update_data(fill_mood=int(message.text))
        await message.answer('Как вы оцениваете своё состояние (бодрость, активность) наутро по шкале от 1 до 10?')
        await FSMFillDiary.next()

    @dp.message_handler(lambda message: not message.text.isdigit() or int(message.text) < 0 or int(message.text) > 10,
                        state=FSMFillDiary.fill_selffeeling_morning)
    async def process_answer_1_10_invalid(message: types.Message):
        return await message.reply("В ответ введите число от 1 до 10")

    @dp.message_handler(lambda message: message.text.isdigit(), state=FSMFillDiary.fill_selffeeling_morning)
    async def process_turn_to_next_step(message: types.Message, state: FSMContext):
        await state.update_data(fill_selffeeling_morning=int(message.text))
        await message.answer('Во сколько вы вчера легли в кровать?(В ответ напишите время в формате 00:00)')
        await FSMFillDiary.next()

    @dp.message_handler(
        lambda message: not len(message.text) == 5 or not message.text[2] == ':' or not message.text.split(':')[
            0].isdigit() or not message.text.split(':')[1].isdigit(),
        state=FSMFillDiary.fill_time_turn_bed)
    async def process_answer_24_format_invalid(message: types.Message):
        return await message.reply("В ответ введите время в 24-х часовом формате, например 00:00")

    @dp.message_handler(
        lambda message: 0 <= int(message.text.split(':')[0]) <= 23 and 0 <= int(message.text.split(':')[1]) <= 59,
        state=FSMFillDiary.fill_time_turn_bed)
    async def process_turn_to_next_step(message: types.Message, state: FSMContext):
        await state.update_data(fill_time_turn_bed=str(message.text))
        await message.answer('Во сколько вы выключили свет и решили заснуть?(В ответ напишите время в формате 00:00)')
        await FSMFillDiary.next()

    @dp.message_handler(
        lambda message: not len(message.text) == 5 or not message.text[2] == ':' or not message.text.split(':')[
            0].isdigit() or not message.text.split(':')[1].isdigit(),
        state=FSMFillDiary.fill_time_turnoff_ligth)
    async def process_answer_24_format_invalid(message: types.Message):
        return await message.reply("В ответ введите время в 24-х часовом формате, например 00:00")

    @dp.message_handler(
        lambda message: 0 <= int(message.text.split(':')[0]) <= 23 and 0 <= int(message.text.split(':')[1]) <= 59,
        state=FSMFillDiary.fill_time_turnoff_ligth)
    async def process_turn_to_next_step(message: types.Message, state: FSMContext):
        await state.update_data(fill_time_turnoff_ligth=str(message.text))
        await message.answer('Сколько примерно у вас ушло времени, чтобы заснуть (в минутах)?')
        await FSMFillDiary.next()

    @dp.message_handler(lambda message: not message.text.isdigit(),
                        state=FSMFillDiary.fill_time_start_sleep_minutes)
    async def process_answer_1_10_invalid(message: types.Message):
        return await message.reply("В ответ введите число минут")

    @dp.message_handler(lambda message: message.text.isdigit(), state=FSMFillDiary.fill_time_start_sleep_minutes)
    async def process_turn_to_next_step(message: types.Message, state: FSMContext):
        await state.update_data(fill_time_start_sleep_minutes=int(message.text))
        await message.answer('Сколько раз вы просыпались среди ночи (до окончательного утреннего пробуждения)?')
        await FSMFillDiary.next()

    @dp.message_handler(lambda message: message.text.isdigit(), state=FSMFillDiary.fill_how_many_wakingups)
    async def process_turn_to_next_step(message: types.Message, state: FSMContext):
        await state.update_data(fill_how_many_wakingups=str(message.text))
        await message.answer('Сколько времени суммарно длились эти пробуждения? (в минутах)')
        await FSMFillDiary.next()

    @dp.message_handler(lambda message: not message.text.isdigit(),
                        state=FSMFillDiary.fill_sum_wakingups_time_minutes)
    async def process_answer_1_10_invalid(message: types.Message):
        return await message.reply("В ответ введите число минут")

    @dp.message_handler(lambda message: message.text.isdigit(), state=FSMFillDiary.fill_sum_wakingups_time_minutes)
    async def process_turn_to_next_step(message: types.Message, state: FSMContext):
        await state.update_data(fill_sum_wakingups_time_minutes=int(message.text))
        await message.answer('Во сколько было ваше финальное пробуждение?(В ответ напишите время в формате 00:00)')
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
        await state.update_data(fill_wakingup_by_alam=callback_data_to_text(str(callback.data)),
                                last_fill_timestap=int(time.time()))
        await bot.send_message(callback.message.chat.id,
                               text='Спасибо за ваше пробуждение',
                               reply_markup=keyboard_start_buttons)

        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()

        print(storage.data[str(callback.message.chat.id)][str(callback.message.chat.id)]['data'])


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
