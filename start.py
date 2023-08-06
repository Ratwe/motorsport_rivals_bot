from telebot import types

from main import bot
import texts
from race import add_race_info


@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Начать')
    markup.add(btn1)
    bot.send_message(message.from_user.id, texts.greetings, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Начать':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        btn1 = types.KeyboardButton(texts.add_race_info)
        markup.add(btn1)
        bot.send_message(message.from_user.id, 'Выберите интересующую вас функцию.', reply_markup=markup)  # ответ бота

    elif message.text == texts.add_race_info:
        add_race_info()