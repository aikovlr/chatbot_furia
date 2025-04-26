
import telebot
from dotenv import load_dotenv
import os
from bot.handlers import registrar_handlers

load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_API_KEY"))
registrar_handlers(bot)
bot.polling()
