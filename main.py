from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os

import nav_constants
from randomizer import Randomizer, wise_list
import keyboards
import messages


load_dotenv()
bot = Bot(
    token=os.getenv('BOT_TOKEN'),
    parse_mode="HTML"
)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message) -> None:
    await message.answer(messages.welcome, reply_markup=keyboards.menu_keyboard)


@dp.message_handler(commands=['about'])
async def about(message: types.Message) -> None:
    await message.answer(messages.about)


@dp.message_handler(text=nav_constants.random_str)
async def menu_keyboard_reaction(message: types.Message) -> None:
    randomizer = Randomizer()
    await message.answer(randomizer.randomize(wise_list))


if __name__ == "__main__":
    executor.start_polling(dp)
