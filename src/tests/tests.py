from src.json_tools import load_race_data_from_json


def load_race_data_from_json_test():
    print("[TEST]: load_race_data_from_json_test(1)")
    race_data = load_race_data_from_json(1)
    race_data[0].print_info()

    print("\n[TEST]: load_race_data_from_json_test(2)")
    race_data = load_race_data_from_json(2)
    for race in race_data:
        race.print_info()

    print("\n[TEST]: load_race_data_from_json_test(0)")
    race_data = load_race_data_from_json(0)
    for race in race_data:
        race.print_info()

    print("\n[TEST]: load_race_data_from_json_test COMPLETED\n")