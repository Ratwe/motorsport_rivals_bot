import json

from config import RACE_DATA_FILENAME


def get_race_data(state):
    race = state.race

    race_data = {
        "race_id": race.race_id,
        "team1": race.team1,
        "team2": race.team2,
        "overtakes_team1": race.overtakes_team1,
        "overtakes_team2": race.overtakes_team2,
        "speed_team1": race.speed_team1,
        "speed_team2": race.speed_team2,
        "scores": race.scores,
        "laps": []
    }

    for lap in race.laps:
        lap_data = {
            "lap_number": lap.number,
            "speed_team1": lap.speed_team1,
            "speed_team2": lap.speed_team2,
            "best_lap": lap.best_lap
        }
        race_data["laps"].append(lap_data)

    return race_data


def save_to_json(state):
    with open(RACE_DATA_FILENAME, "r") as json_file:
        all_data = json.load(json_file)

    all_data.append(get_race_data(state))

    with open(RACE_DATA_FILENAME, "w") as json_file:
        json.dump(all_data, json_file, indent=4)
