from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
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
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class StoryPipeline(StatesGroup):
    next_step = State()


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message) -> None:
    await message.answer(messages.welcome, reply_markup=keyboards.menu_keyboard)


@dp.message_handler(commands=['about'])
async def about(message: types.Message) -> None:
    await message.answer(f"Пайплайн начался!\n\n{messages.first_item}", reply_markup=keyboards.next_step_keyboard)
    await StoryPipeline.next_step.set()


@dp.callback_query_handler(text="next_step_button", state=StoryPipeline.next_step)
async def send_text(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        try:
            pipeline_index = data['iterator']
        except KeyError:
            data['iterator'] = 0
            pipeline_index = data['iterator']

        try:
            await call.message.edit_text(messages.about[pipeline_index], reply_markup=keyboards.next_step_keyboard)
            data['iterator'] = pipeline_index + 1
        except IndexError:
            await call.message.delete_reply_markup()
            await call.message.answer("Пайплайн пройден!")
            await state.finish()


@dp.message_handler(text=nav_constants.random_str)
async def menu_keyboard_reaction(message: types.Message) -> None:
    randomizer = Randomizer()
    await message.answer(randomizer.randomize(wise_list))


if __name__ == "__main__":
    executor.start_polling(dp)
