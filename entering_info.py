from telebot import types

import texts
from checkouts import check_overtakes, check_values
from config import CLUBS
from errors import LAST_LAP
from globals import user_states, bot


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