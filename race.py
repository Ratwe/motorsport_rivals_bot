from telebot import types

from config import CLUBS
from main import bot
import texts


@bot.message_handler(content_types=['text'])
def enter_club(message):
    bot.send_message(texts.enter_club_name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок

    markup.add(types.KeyboardButton(club) for club in CLUBS)

    bot.send_message(message.from_user.id, texts.choose_option, reply_markup=markup)  # ответ бота

    print(f"Ваш клуб -- {message.text}")


@bot.message_handler(content_types=['text'])
def add_race_info(message):
    enter_club(message)
