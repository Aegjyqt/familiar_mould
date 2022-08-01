from aiogram.utils.markdown import hbold, hlink, hcode, hitalic, hstrikethrough, hspoiler


welcome = f"{hbold('This is a welcome message')}"
link = hlink(title="Ссылка", url="https://google.com")

# <b>Жирный</b>
# <i>Курсив</i>
# <code>Моноширинный с возможностью копирования</code>
# <tg-spoiler>Скрытый текст</tg-spoiler>

about = 'Here will be the bot description'
