import telebot
from telebot import types

import texts
from config import TOKEN, CLUBS
from classes import Race, UserState

bot = telebot.TeleBot(TOKEN)

user_states = {}  # Словарь для хранения состояний пользователей


def enter_club(message):
    user_id = message.from_user.id
    user_states[user_id].entering_race_info = True
    bot.send_message(user_id, texts.enter_club_name)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for club in CLUBS:
        markup.add(types.KeyboardButton(club))


def enter_team1(message):
    user_id = message.from_user.id
    user_states[user_id].entering_race_info = False
    user_states[user_id].entering_team1 = True

    user_states[user_id].race.team1 = message.text

    bot.send_message(message.from_user.id, texts.enter_race_team2)



def enter_team2(message):
    user_id = message.from_user.id
    user_states[user_id].entering_team1 = False
    user_states[user_id].entering_team2 = True

    user_states[user_id].race.team2 = message.text

    bot.send_message(message.from_user.id, texts.enter_race_overtakes1)




def enter_overtakes1(message):
    user_id = message.from_user.id
    user_states[user_id].entering_team2 = False
    user_states[user_id].entering_overtakes1 = True

    user_states[user_id].race.overtakes_team1 = int(message.text)

    bot.send_message(message.from_user.id, texts.enter_race_overtakes2)



def enter_overtakes2(message):
    user_id = message.from_user.id
    user_states[user_id].entering_overtakes1 = False
    user_states[user_id].entering_overtakes2 = True

    user_states[user_id].race.overtakes_team2 = int(message.text)

    bot.send_message(message.from_user.id, texts.enter_laps)




def enter_laps(message):
    pass


@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Начать')
    markup.add(btn1)
    bot.send_message(message.from_user.id, texts.greetings, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_messages(message):
    user_id = message.from_user.id

    print(f"message.text = {message.text}")

    if message.text == 'Начать':
        user_states[user_id] = UserState()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(texts.add_race_info)
        markup.add(btn1)
        bot.send_message(user_id, texts.choose_option, reply_markup=markup)

    elif message.text == texts.add_race_info or message.text == 'add':
        user_states[user_id] = UserState()
        user_states[user_id].entering_race_info = True

        bot.send_message(user_id, texts.enter_race)
        bot.send_message(message.from_user.id, texts.enter_race_team1)

    elif user_id in user_states:
        state = user_states[user_id]

        if state.entering_race_info:
            enter_team1(message)

        elif state.entering_team1:
            enter_team2(message)

        elif state.entering_team2:
            enter_overtakes1(message)

        elif state.entering_overtakes1:
            enter_overtakes2(message)

        elif state.entering_overtakes2:
            enter_laps(message)
            user_states[user_id].race.print_info()


bot.infinity_polling()  # обязательная для работы бота часть
