import collecting
from classes import UserState

from entering_info import *
from globals import bot


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
        btn = types.KeyboardButton(texts.add_race_info)
        markup.add(btn)
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
                race_info = state.race.get_info_as_text()
                bot.send_message(user_id, race_info)

            collecting.save_to_json(state)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton(texts.begin)
            markup.add(btn)
            bot.send_message(user_id, texts.rerun_states, reply_markup=markup)

            state.printing_info = False


bot.infinity_polling()  # обязательная для работы бота часть
