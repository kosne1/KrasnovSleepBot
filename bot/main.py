# from prisma import PrismaClient
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import *
from config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class FSMFillDiary(StatesGroup):
    fill_quality_sleep = State()
    fill_drowsiness = State()
    fill_mood_last_day = State()
    fill_selffeeling_morning = State()
    fill_time_turn_bed = State()
    fill_time_turnoff_ligth= State()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(text='''Добро пожаловать в бот Dreamy, придуманный @sasha_krasnow для помощи при бессоннице!\n\nВыберите одну из опций''',
                         reply_markup=keyboard_start_buttons)

    @dp.message_handler(Text('Заполнить дневник сна'))
    async def start_filling_diary(message: Message):
        await FSMFillDiary.fill_quality_sleep.set()
        await message.reply('Как вы оцениваете своё сегодняшнее качество сна от 1 до 10 ?')

    @dp.message_handler(state='*', commands='cancel')
    @dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
    async def cancel_handler(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return

        await state.finish()
        # And remove keyboard (just in case)
        await message.reply('Заполнение дневника отменено', reply_markup=types.ReplyKeyboardRemove())


        @dp.message_handler(lambda message: not message.text.isdigit(), state=FSMFillDiary.fill_quality_sleep)
        async def process_age_invalid(message: types.Message):

            return await message.reply("В ответ введите число от 1 до 10")

        @dp.message_handler(lambda message: message.text.isdigit(), state=FSMFillDiary.fill_quality_sleep)
        async def process_age(message: types.Message, state: FSMContext):
            # Update state and data
            await state.update_data(age=int(message.text))
            await message.reply('Как вы оцениваете свою сонливость вчера в течение дня по шкале от 1 до 10?')
            await FSMFillDiary.next()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
