LAP_NUM_ERR = 1
VALUES_LEN_ERR = 2
LAST_LAP = 3
LAP_DUPLICATE_ERR = 4

BEST_LAP_VAL_ERR = 5
CONV_ERR = 6
SPEED_VAL_ERR = 7

EXIT_SUCCESS = 0


def get_err_code_message(err_code):
    match err_code:
        case 1:
            return "Ошибка! Номер круга должен быть в диапазоне от 1 до 15"
        case 2:
            return ("Ошибка! Ожидается четыре величины: номер круга, скорость первой команды, скорость второй команды, "
                    "идеальный ли круг")
        case 5:
            return "Ошибка! Значение идеального круга может быть или 0 (не идеальный круг) или 1 (идеальный круг)"
        case 6:
            return "Ошибка приведения типа! Убедитесь, что вам нужно ввести: может быть, вы вводите слово вместо числа?"
        case 7:
            return "Ошибка! Скорость должна быть больше нуля"
        case _:
            return "Неизвестная ошибка!"