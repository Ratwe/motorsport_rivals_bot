import json

from config import RACE_DATA_FILENAME
from validation.errors import *


def race_exists(race_id):
    try:
        with open(RACE_DATA_FILENAME, "r") as json_file:
            data = json.load(json_file)
            for race in data:
                if race["race_id"] == race_id:
                    return True
            return False
    except FileNotFoundError:
        return False


def check_overtakes(text):
    try:
        int(text)
    except:
        return CONV_ERR

    return EXIT_SUCCESS


def check_lap_num(num, laps):
    for lap in laps:
        if lap.number == num:
            return LAP_DUPLICATE_ERR

    return EXIT_SUCCESS


def check_values(values, laps):
    if len(values) != 4:
        return VALUES_LEN_ERR

    try:
        for i in range(len(values)):
            values[i] = int(values[i])
    except:
        return CONV_ERR

    if values[0] > 15:
        return LAP_NUM_ERR

    if values[0] == 15:
        return LAST_LAP

    if not (0 <= values[3] <= 1):
        return BEST_LAP_VAL_ERR

    if values[1] * values[2] <= 0:
        return SPEED_VAL_ERR

    if check_lap_num(values[0], laps):
        return LAP_DUPLICATE_ERR

    return EXIT_SUCCESS


def check_count(num):
    try:
        num = int(num)
    except:
        return CONV_ERR

    if num <= 0:
        return RACES_NUM_ERR

    return EXIT_SUCCESS