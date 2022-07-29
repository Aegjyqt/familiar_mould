from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

# целесообразно ли создать класс Keyboard для генерации keyboards по заданным параметрам?

button1 = InlineKeyboardButton(text='get random str')
button2 = InlineKeyboardButton(text='get essential data')
button3 = InlineKeyboardButton(text='request support')
button4 = InlineKeyboardButton(text='questboard')
button5 = InlineKeyboardButton(text='reminder')
button6 = InlineKeyboardButton(text='settings')

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).\
                                    add(button1, button2, button3, button4, button5, button6)

