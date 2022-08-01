from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os

import nav_constants
import randomizer
from randomizer import Randomizer

import keyboards
import messages

load_dotenv()
bot = Bot(os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer(messages.welcome, reply_markup=keyboards.menu_keyboard)


@dp.message_handler(commands=['about'])
async def about(message: types.Message):
    await message.answer(messages.about)


@dp.message_handler(text=nav_constants.random_str)  # у меня на записи не видно подробностей (как перегнать в text=Text)
async def menu_keyboard_reaction(message: types.Message) -> None:
    await message.answer(Randomizer(randomizer.wise_list).randomize(randomizer.wise_list))


executor.start_polling(dp)
