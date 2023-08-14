from src.calculations.stats import calc_average_stats
from src.globals import user_states, bot
from src.json_tools import load_race_data_from_json
from src.validation.checkouts import check_count
from src.validation.errors import get_err_code_message


def get_average_stats(message):
    user_id = message.from_user.id
    state = user_states[user_id]

    err_code = check_count(message.text)
    if err_code:
        bot.send_message(user_id, get_err_code_message(err_code))
        return

    count = int(message.text)

    state.getting_average_stats = False

    stats = calc_average_stats(count)

    return stats


def get_races_data(message):
    print(f"user_states = {user_states}")
    user_id = message.from_user.id
    state = user_states[user_id]

    err_code = check_count(message.text)
    if err_code:
        bot.send_message(user_id, get_err_code_message(err_code))
        return

    count = int(message.text)

    state.getting_races_data = False

    races_data = load_race_data_from_json(count)

    return races_data


def print_average_stats(stats):
    pass


