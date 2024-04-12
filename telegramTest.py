# pip install python-telegram-bot

import telegram
import asyncio

bot = telegram.Bot(token="**********")
chat_id = "*******"

asyncio.run(bot.sendMessage(chat_id=chat_id, text="Good Morning, My Python Telegram"))