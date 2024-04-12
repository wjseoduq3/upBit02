# pip install python-telegram-bot

import telegram
import asyncio

bot = telegram.Bot(token="7150770982:AAFSa3on25LTmBtIDDr9eqL8kleAtPiq7EI")
chat_id = "7159357052"

asyncio.run(bot.sendMessage(chat_id=chat_id, text="Good Morning, My Python Telegram"))