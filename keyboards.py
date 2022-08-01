from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

import nav_constants


menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=nav_constants.random_str),
            KeyboardButton(text=nav_constants.essential_data)
        ],
        [
            KeyboardButton(text=nav_constants.request_support),
            KeyboardButton(text=nav_constants.questboard)
        ],
        [
            KeyboardButton(text=nav_constants.reminder),
            KeyboardButton(text=nav_constants.settings)
        ]
    ],
    resize_keyboard=True
)
