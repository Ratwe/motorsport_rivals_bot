import telebot

from config import TOKEN

bot = telebot.TeleBot(TOKEN)
user_states = {}  # Словарь для хранения состояний пользователей
