from calculations.stats import calc_average_race
from globals import user_states, bot
from json_tools import load_race_data_from_json
from validation.checkouts import check_count
from validation.errors import get_err_code_message


def get_average_race(message):
    user_id = message.from_user.id
    state = user_states[user_id]

    err_code = check_count(message.text)
    if err_code:
        bot.send_message(user_id, get_err_code_message(err_code))
        return

    count = int(message.text)

    races_list = load_race_data_from_json(count)
    avg_race = calc_average_race(races_list)

    avg_race_info = avg_race.get_info_as_text(full=state.mode_full)
    bot.send_message(user_id, avg_race_info)

    state.getting_average_race = False



def get_races_data(message):
    user_id = message.from_user.id
    state = user_states[user_id]

    err_code = check_count(message.text)
    if err_code:
        bot.send_message(user_id, get_err_code_message(err_code))
        return

    count = int(message.text)

    races_list = load_race_data_from_json(count)
    for race in races_list:
        race_info = race.get_info_as_text(full=state.mode_full)
        bot.send_message(user_id, race_info)

    state.getting_races_data = False

