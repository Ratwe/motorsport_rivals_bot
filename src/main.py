import texts
from classes.user_state import UserState
from info_collectors.entering_info import *
from info_collectors.saving_info import save_to_json
from globals import bot, user_states
from validation.checkouts import race_exists


@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton(texts.begin)
    markup.add(btn)
    bot.send_message(message.from_user.id, texts.greetings, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_messages(message):
    user_id = message.from_user.id

    print(f"message.text = {message.text}")

    if message.text == texts.begin:
        user_states[user_id] = UserState()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(texts.add_race_info)
        btn2 = types.KeyboardButton(texts.get_average_stats)
        markup.add(btn1, btn2)
        bot.send_message(user_id, texts.choose_option, reply_markup=markup)

    elif message.text == texts.add_race_info or message.text == 'add':
        user_states[user_id] = UserState()
        user_states[user_id].entering_race_info = True

        bot.send_message(user_id, texts.enter_race, reply_markup=None)
        bot.send_message(user_id, texts.enter_race_team1)

    elif message.text == texts.get_average_stats or message.text == 'stat':
        user_states[user_id] = UserState()
        user_states[user_id].getting_average_stats = True

        bot.send_message(user_id, texts.enter_races_count, reply_markup=None)

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

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton(texts.begin)
            markup.add(btn)
            bot.send_message(user_id, texts.rerun_states, reply_markup=markup)

            state.printing_info = False

        elif state.getting_average_stats:
            get_average_stats(message)



bot.infinity_polling()  # обязательная для работы бота часть
