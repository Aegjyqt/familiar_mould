from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile
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


class Profile(StatesGroup):
    name = State()
    surname = State()
    photo = State()
    age = State()


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message) -> None:
    await message.answer("Хендлер сработал")
    await message.answer(messages.welcome, reply_markup=keyboards.menu_keyboard)


@dp.message_handler(commands=['about'])
async def about(message: types.Message) -> None:
    await message.answer(f"", reply_markup=keyboards.next_step_keyboard)


@dp.message_handler(commands=['form'])
async def start_form(message: types.Message) -> None:
    await message.answer("<b>Начало анкеты.</b>\n\nВведи свое имя:")
    await Profile.name.set()


@dp.message_handler(state=Profile.name)
async def handle_entered_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text
        msg_id = (await message.answer_photo(photo=InputFile("person_avatar.webp"),
                                             caption=messages.get_caption(name=message.text))).message_id
        data['msg_id'] = msg_id
    await state.set_state(Profile.surname)


@dp.message_handler(state=Profile.surname)
async def handle_entered_surname(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['surname'] = message.text
        await message.bot.edit_message_caption(chat_id=message.from_user.id,
                                               message_id=data['msg_id'],
                                               caption=messages.get_caption(name=data['name'], surname=data['surname']))
    await state.set_state(Profile.age)


@dp.message_handler(state=Profile.age)
async def handle_entered_age(message: types.Message, state: FSMContext) -> None:
    entered_age = message.text
    try:
        entered_age = int(entered_age)
    except ValueError:
        await message.reply("Ввод некорректен. Еще раз введи свой возраст")
        return

    async with state.proxy() as data:
        data['age'] = entered_age

    await message.answer("Отлично. Теперь пришли свою фотографию:")
    await state.set_state(Profile.photo)


@dp.message_handler(state=Profile.photo, content_types=['photo'])
async def handle_sent_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        sent_photo_id = message.photo[-1].file_id
        user_name = data['name']
        user_surname = data['surname']
        user_age = data['age']
        await message.answer_photo(
            photo=sent_photo_id,
            caption=f"Имя: {user_name}\nФамилия: {user_surname}\nВозраст: {user_age}")

    await state.finish()


@dp.message_handler(text=nav_constants.random_str)
async def menu_keyboard_reaction(message: types.Message) -> None:
    randomizer = Randomizer()
    await message.answer(randomizer.randomize(wise_list))


if __name__ == "__main__":
    executor.start_polling(dp)
