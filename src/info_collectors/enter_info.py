from telebot import types

import texts
from globals import user_states, bot
from validation.checkouts import check_overtakes, check_values
from validation.errors import get_err_code_message, LAST_LAP


def enter_team1(message):
    user_id = message.from_user.id
    state = user_states[user_id]
    state.entering_race_info = False
    state.entering_team1 = True

    state.race.team1 = message.text.lower()

    bot.send_message(message.from_user.id, texts.enter_race_team2)


def enter_team2(message):
    user_id = message.from_user.id
    state = user_states[user_id]
    state.entering_team1 = False
    state.entering_team2 = True

    state.race.team2 = message.text.lower()

    bot.send_message(message.from_user.id, texts.enter_race_overtakes1)


def enter_overtakes1(message):
    err_code = check_overtakes(message.text)
    if err_code:
        bot.send_message(message.from_user.id, get_err_code_message(err_code))
        return

    user_id = message.from_user.id
    state = user_states[user_id]
    state.entering_team2 = False
    state.entering_overtakes1 = True

    state.race.overtakes_team1 = int(message.text)

    bot.send_message(message.from_user.id, texts.enter_race_overtakes2)


def enter_overtakes2(message):
    if check_overtakes(message.text):
        return

    user_id = message.from_user.id
    state = user_states[user_id]
    state.entering_overtakes1 = False
    state.entering_overtakes2 = True

    state.race.overtakes_team2 = int(message.text)

    bot.send_message(message.from_user.id, texts.enter_laps)
    bot.send_message(user_id, texts.enter_laps_template, parse_mode='Markdown')
    bot.send_message(user_id, texts.enter_laps_example, parse_mode='Markdown')

    example_images = [types.InputMediaPhoto('https://github.com/Ratwe/motorsport_rivals_bot/blob/master/images/enter_laps_template1.jpg?raw=true',
                                            caption=texts.example_images_caption),
                      types.InputMediaPhoto('https://github.com/Ratwe/motorsport_rivals_bot/blob/master/images/enter_laps_template2.jpg?raw=true'),
                      types.InputMediaPhoto('https://github.com/Ratwe/motorsport_rivals_bot/blob/master/images/enter_laps_template3.jpg?raw=true')]

    bot.send_media_group(user_id, example_images)


def enter_laps(message):
    user_id = message.from_user.id
    state = user_states[user_id]
    if state.entering_overtakes2:
        state.race.laps = []
        state.entering_overtakes2 = False

    state.entering_laps = True

    values = message.text.split()
    err_code = check_values(values, state.race.laps)

    if err_code == LAST_LAP:
        state.entering_laps = False
        state.printing_info = True

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(texts.yes)
        btn2 = types.KeyboardButton(texts.no)
        markup.add(btn1, btn2)

        bot.send_message(user_id, texts.ask_print_race_info, reply_markup=markup)

    elif err_code:
        bot.send_message(user_id, get_err_code_message(err_code))
        return

    lap_data = {
        'lap_number': int(values[0]),
        'speed_team1': int(values[1]),
        'speed_team2': int(values[2]),
        'best_lap': bool(values[3])
    }

    state.race.add_lap(lap_data)

