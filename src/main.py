from telebot import types

import texts
from classes.user_state import UserState
from globals import bot, user_states
from src.info_collectors.enter_info import enter_team1, enter_team2, enter_overtakes1, enter_overtakes2, enter_laps
from src.info_collectors.get_info import get_average_stats, get_races_data
from src.json_tools import save_to_json
from src.tests.tests import load_race_data_from_json_test
from validation.checkouts import race_exists, check_count


@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton(texts.begin)
    markup.add(btn)
    bot.send_message(message.from_user.id, texts.greetings, reply_markup=markup)

def rerun(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton(texts.begin)
    markup.add(btn)
    bot.send_message(user_id, texts.rerun_states, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_messages(message):
    user_id = message.from_user.id

    print(f"message.text = {message.text}")

    if message.text == texts.begin:
        user_states[user_id] = UserState()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(texts.add_race_info)
        btn2 = types.KeyboardButton(texts.get_stats)
        markup.add(btn1, btn2)
        bot.send_message(user_id, texts.choose_option, reply_markup=markup)

    elif message.text == texts.add_race_info or message.text == 'add':
        user_states[user_id] = UserState()
        user_states[user_id].entering_race_info = True

        bot.send_message(user_id, texts.enter_race, reply_markup=None)
        bot.send_message(user_id, texts.enter_race_team1)

    elif message.text == texts.get_stats or message.text == 'stats':
        user_states[user_id] = UserState()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(texts.get_races_data)
        btn2 = types.KeyboardButton(texts.get_average_stats)
        markup.add(btn1, btn2)
        bot.send_message(user_id, texts.choose_option, reply_markup=markup)

    elif message.text == texts.get_average_stats or message.text == 'stat avg':
        user_states[user_id] = UserState()
        user_states[user_id].getting_average_stats = True

        bot.send_message(user_id, texts.enter_races_count, reply_markup=None)

    elif message.text == texts.get_races_data or message.text == 'stat raw':
        user_states[user_id] = UserState()
        user_states[user_id].getting_races_data = True

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(texts.yes)
        btn2 = types.KeyboardButton(texts.no)
        markup.add(btn1, btn2)
        bot.send_message(user_id, texts.ask_print_laps_info, reply_markup=markup)


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
            state.race.calculate_speed()
            state.race.calculate_score()
            state.race.calculate_race_id()

            if race_exists(state.race.race_id):
                bot.send_message(user_id, texts.race_exists)
                state.printing_info = False
                return

            if message.text == texts.yes:
                race_info = state.race.get_info_as_text()
                bot.send_message(user_id, race_info)

            print(state.race.get_info_as_text())

            save_to_json(state)

            state.printing_info = False

            rerun(user_id)


        elif state.getting_races_stats:
            pass

        elif state.getting_races_data or state.getting_average_stats:
            if state.mode_full is None:
                state.mode_full = (message.text == texts.yes)
                bot.send_message(user_id, texts.enter_races_count, reply_markup=None)
            else:
                if state.getting_average_stats:
                    get_average_stats(message)
                elif state.getting_races_data:
                    get_races_data(message)

                state.getting_average_stats = False
                state.getting_races_data = False
                state.mode_full = None

                rerun(user_id)


bot.infinity_polling()  # обязательная для работы бота часть
