import telebot
from telebot import types

import texts
from config import TOKEN, CLUBS
from classes import Race, UserState, Lap
from errors import *

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


def check_overtakes(text):
    try:
        int(text)
    except:
        return OVERTAKE_TYPE_ERR

    return EXIT_SUCCESS


def enter_overtakes1(message):
    if check_overtakes(message.text):
        return

    user_id = message.from_user.id
    user_states[user_id].entering_team2 = False
    user_states[user_id].entering_overtakes1 = True

    user_states[user_id].race.overtakes_team1 = int(message.text)

    bot.send_message(message.from_user.id, texts.enter_race_overtakes2)



def enter_overtakes2(message):
    if check_overtakes(message.text):
        return

    user_id = message.from_user.id
    user_states[user_id].entering_overtakes1 = False
    user_states[user_id].entering_overtakes2 = True

    user_states[user_id].race.overtakes_team2 = int(message.text)

    bot.send_message(message.from_user.id, texts.enter_laps)
    bot.send_message(user_id, texts.enter_laps_template, parse_mode='Markdown')
    bot.send_message(user_id, texts.enter_laps_example, parse_mode='Markdown')


def check_values(values):
    if len(values) != 4:
        return VALUES_LEN_ERR

    if int(values[0]) > 15:
        return LAP_NUM_ERR

    if int(values[0]) == 15:
        return LAST_LAP

    return EXIT_SUCCESS


def enter_laps(message):
    user_id = message.from_user.id
    state = user_states[user_id]
    state.entering_overtakes2 = False
    state.entering_laps = True

    values = message.text.split()
    err_code = check_values(values)

    if err_code == LAST_LAP:
        state.entering_laps = False
        state.printing_info = True

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(texts.yes)
        btn2 = types.KeyboardButton(texts.no)
        markup.add(btn1, btn2)

        bot.send_message(user_id, texts.ask_print_race_info, reply_markup=markup)

    elif err_code:
        state.entering_laps = False
        return


    lap_data = {
        'lap_number': int(values[0]),
        'speed_team1': int(values[1]),
        'speed_team2': int(values[2]),
        'best_lap': bool(values[3])
    }

    state.race.add_lap(lap_data)



@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(texts.begin)
    markup.add(btn1)
    bot.send_message(message.from_user.id, texts.greetings, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_messages(message):
    user_id = message.from_user.id

    print(f"message.text = {message.text}")

    if message.text == texts.begin:
        user_states[user_id] = UserState()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(texts.add_race_info)
        markup.add(btn1)
        bot.send_message(user_id, texts.choose_option, reply_markup=markup)

    elif message.text == texts.add_race_info or message.text == 'add':
        user_states[user_id] = UserState()
        user_states[user_id].entering_race_info = True

        bot.send_message(user_id, texts.enter_race, reply_markup=None)
        bot.send_message(user_id, texts.enter_race_team1)

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

        elif state.entering_overtakes2 or state.entering_laps:
            enter_laps(message)

        elif state.printing_info:
            if message.text == texts.yes:
                state.race.print_info()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(texts.begin)
            markup.add(btn1)
            bot.send_message(user_id, texts.rerun_states, reply_markup=markup)

            state.printing_info = False




bot.infinity_polling()  # обязательная для работы бота часть
