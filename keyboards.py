from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

import nav_constants
# целесообразно ли создать класс Keyboard для генерации keyboards по заданным параметрам?

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_about = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="next", callback_data="button_next_pressed"),
            InlineKeyboardButton(text="cancel", callback_data="button_cancel_pressed")
        ]
    ]
)

kb_profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="next", callback_data="button_next_pressed"),
            InlineKeyboardButton(text="cancel", callback_data="button_cancel_pressed")
        ]
    ]
)
