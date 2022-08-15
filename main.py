from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile, InputMediaPhoto
from dotenv import load_dotenv
import os

import nav_constants
# from decorator import admin
from randomizer import Randomizer, wise_list
import keyboards
import messages


load_dotenv()
bot = Bot(
    token=os.getenv('BOT_TOKEN'),
    parse_mode="HTML"
)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class ProfilePipeline(StatesGroup):
    init_state = State()
    name_state = State()
    age_state = State()
    photo_state = State()

class AboutPipeline(StatesGroup):
    next_step = State()


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message) -> None:
    await message.answer(f'{message.from_user.first_name}, ' + messages.welcome)


@dp.message_handler(commands='about')
async def send_about(message: types.Message) -> None:
    await message.answer(messages.about_openline, reply_markup=keyboards.kb_about)
    await AboutPipeline.next_step.set()


@dp.callback_query_handler(text="button_next_pressed", state=AboutPipeline.next_step)
async def next_pressed(call: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        try:
            pipeline_index = data['iterator']
        except KeyError:
            data['iterator'] = 0
            pipeline_index = data['iterator']

        try:
            await call.message.answer(messages.about_list[pipeline_index], reply_markup=keyboards.kb_about)
            data['iterator'] = pipeline_index + 1
            await call.message.delete_reply_markup()
        except IndexError:
            await call.message.delete_reply_markup()
            await call.message.answer("about message finished")
            await state.finish()


@dp.callback_query_handler(text="button_cancel_pressed", state=AboutPipeline.next_step)
async def cancel_pressed(call: types.CallbackQuery, state=FSMContext) -> None:
    await call.message.reply(text="you pressed cancel")
    await call.message.delete_reply_markup()
    await state.finish()


@dp.message_handler(commands='profile')
async def profile_pipeline_start(message: types.Message) -> None:
    await message.answer(text='Fill the data for your profile?', reply_markup=keyboards.kb_profile)
    await ProfilePipeline.init_state.set()


@dp.callback_query_handler(text="button_next_pressed", state=ProfilePipeline.init_state)
async def profile_pipeline_next_pressed(call: types. CallbackQuery, state=FSMContext) -> None:
    async with state.proxy() as data:
        profile_init_msg_id = (await bot.send_photo(photo=InputFile("photo_placeholder.jpg"), chat_id=call.from_user.id,
                                                    caption=messages.get_caption())).message_id
        data['profile_init_msg_id'] = profile_init_msg_id
        profile_init_msg2_id = (await bot.send_message(text="Enter your name:", chat_id=call.from_user.id)).message_id
        data['profile_init_msg2_id'] = profile_init_msg2_id
    await state.set_state(ProfilePipeline.name_state)


@dp.callback_query_handler(text="button_cancel_pressed", state=ProfilePipeline.init_state)
async def cancel_pressed(call: types.CallbackQuery, state=FSMContext) -> None:
    await call.message.reply(text="you pressed cancel")
    await call.message.delete_reply_markup()
    await state.finish()


@dp.message_handler(state=ProfilePipeline.name_state)
async def name_state_process(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        await bot.delete_message(message_id=data['profile_init_msg2_id'], chat_id=message.from_user.id)
        await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
        data['name'] = message.text
        await message.bot.edit_message_caption(chat_id=message.from_user.id,
                                               message_id=data['profile_init_msg_id'],
                                               caption=messages.get_caption(name=data['name']))
        profile_name_msg_id = (await message.answer(text='Enter your age:')).message_id
        data['profile_name_msg_id'] = profile_name_msg_id
    await state.set_state(ProfilePipeline.age_state)


@dp.message_handler(state=ProfilePipeline.age_state)
async def age_state_process(message: types.Message, state: FSMContext) -> None:
    entered_age = message.text
    try:
        entered_age = int(entered_age)
    except ValueError:
        await message.reply("Incorrect input. Enter your age")
        return
    async with state.proxy() as data:
        await bot.delete_message(message_id=data['profile_name_msg_id'], chat_id=message.from_user.id)
        await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
        data['age'] = message.text
        await message.bot.edit_message_caption(chat_id=message.from_user.id,
                                               message_id=data['profile_init_msg_id'],
                                               caption=messages.get_caption(name=data['name'], age=data['age']))
        profile_age_msg_id = (await message.answer(text='Send photo:')).message_id
        data['profile_age_msg_id'] = profile_age_msg_id
    await state.set_state(ProfilePipeline.photo_state)


@dp.message_handler(state=ProfilePipeline.photo_state, content_types='photo')
async def photo_state_process(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        await bot.delete_message(message_id=data['profile_age_msg_id'], chat_id=message.from_user.id)
        await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
        sent_photo_id = message.photo[-1].file_id
        await message.bot.edit_message_media(chat_id=message.chat.id,
                                             message_id=data['profile_init_msg_id'],
                                             media=InputMediaPhoto(
                                                media=sent_photo_id,
                                                caption=messages.get_caption(name=data['name'], age=data['age'])))
    await message.answer(text='Profile complete!')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)