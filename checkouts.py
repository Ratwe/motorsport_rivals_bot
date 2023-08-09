from errors import *


def check_overtakes(text):
    try:
        int(text)
    except:
        return OVERTAKE_TYPE_ERR

    return EXIT_SUCCESS


def check_values(values):
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

    return EXIT_SUCCESS
