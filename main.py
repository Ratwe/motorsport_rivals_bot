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


def enter_team1(message, race):
    user_id = message.from_user.id
    user_states[user_id].entering_race_info = False
    user_states[user_id].entering_team1 = True

    team1 = message.text
    race.team1 = team1

    bot.send_message(message.from_user.id, texts.enter_race_team2)



def enter_team2(message, race):
    user_id = message.from_user.id
    user_states[user_id].entering_team1 = False
    user_states[user_id].entering_team2 = True

    team2 = message.text
    race.team2 = team2


def enter_overtakes(message, race):
    user_id = message.from_user.id
    user_states[user_id].entering_overtakes = True
    user_states[user_id].entering_teams = False

    bot.send_message(message.from_user.id, texts.enter_race_overtakes1)
    overtakes_team1 = int(message.text)

    bot.send_message(message.from_user.id, texts.enter_race_overtakes2)
    overtakes_team2 = int(message.text)

    race.overtakes_team1 = overtakes_team1
    race.overtakes_team2 = overtakes_team2


def enter_laps(message, race):
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

    elif user_id in user_states:
        state = user_states[user_id]
        state.print_info()

        race = Race("team1", "team2")

        if state.entering_race_info:
            enter_team1(message, race)

        elif state.entering_team1:
            enter_team2(message, race)
            race.print_info()

        elif state.entering_team2:
            enter_overtakes(message, race)
            race.print_info()


        elif state.entering_overtakes:
            enter_laps(message, race)
            race.print_info()


    elif message.text == texts.add_race_info:
        user_states[user_id] = UserState()
        user_states[user_id].entering_race_info = True
        bot.send_message(user_id, texts.enter_race)
        bot.send_message(message.from_user.id, texts.enter_race_team1)


bot.infinity_polling()  # обязательная для работы бота часть
