from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

import nav_constants
# целесообразно ли создать класс Keyboard для генерации keyboards по заданным параметрам?

button1 = KeyboardButton(text=nav_constants.random_str)
button2 = KeyboardButton(text=nav_constants.essential_data)
button3 = KeyboardButton(text=nav_constants.request_support)
button4 = KeyboardButton(text=nav_constants.questboard)
button5 = KeyboardButton(text=nav_constants.reminder)
button6 = KeyboardButton(text=nav_constants.settings)

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

next_step_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        # Ряд
        [
            InlineKeyboardButton(text="Далее", callback_data="next_step_button")
        ]
    ]
)

