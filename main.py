from aiogram import Bot, Dispatcher,types, executor
from dotenv import load_dotenv
import os
import messages

load_dotenv()
bot = Bot(os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer(messages.welcome) # а вот здесь нужны TypeHints, или и так ясно?

@dp.message_handler(commands=['about'])
async def about(message: types.Message):
    await message.answer(messages.about)

executor.start_polling(dp)