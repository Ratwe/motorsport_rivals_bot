import telebot
from telebot import types

import texts
from config import TOKEN, CLUBS

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def enter_club(message):
    bot.send_message(message.from_user.id, texts.enter_club_name)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    for club in CLUBS:
        markup.add(types.KeyboardButton(club))

    bot.send_message(message.from_user.id, texts.choose_option, reply_markup=markup)  # ответ бота

    print(f"Ваш клуб -- {message.text}")


@bot.message_handler(content_types=['text'])
def add_race_info(message):
    enter_club(message)



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
        bot.send_message(message.from_user.id, texts.choose_option, reply_markup=markup)  # ответ бота

    elif message.text == texts.add_race_info:
        add_race_info()


bot.infinity_polling()  # обязательная для работы бота часть
