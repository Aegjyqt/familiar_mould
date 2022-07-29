from aiogram import Bot, Dispatcher,types, executor
from dotenv import load_dotenv
import os

import get_random_string
from get_random_string import Randomizer

import keyboards
import messages

load_dotenv()
bot = Bot(os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer(messages.welcome, reply_markup=keyboards.menu_keyboard) # а вот здесь нужны TypeHints, или и так ясно?

@dp.message_handler(commands=['about'])
async def about(message: types.Message):
    await message.answer(messages.about)

@dp.message_handler() # как можно "вынести" работу этого (кстати что это? handler?) куда-нибудь, чтобы код не "разбухал"?
async def menu_keyboard_reaction(message: types.Message): # а вот здесь нужны TypeHints, или и так ясно?
    if message.text == 'get random str':
        await message.answer(Randomizer(get_random_string.wise_list).get_random())


executor.start_polling(dp)