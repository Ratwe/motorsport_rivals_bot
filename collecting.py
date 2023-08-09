import hashlib
import json


def save_to_json(state):
    race_data = {
        "team1": state.race.team1,
        "team2": state.race.team2,
        "overtakes_team1": state.race.overtakes_team1,
        "overtakes_team2": state.race.overtakes_team2,
        "scores": state.race.scores,
        "laps": []
    }

    for lap in state.race.laps:
        lap_data = {
            "lap_number": lap.number,
            "speed_team1": lap.speed_team1,
            "speed_team2": lap.speed_team2,
            "best_lap": lap.best_lap
        }
        race_data["laps"].append(lap_data)

    with open("race_data.json", "w") as json_file:
        json.dump(race_data, json_file)


def calculate_race_id(team1_speed, team2_speed, overtakes, laps):
    # Объединяем скорости команд и характеристики гонки
    combined_data = f"{team1_speed}-{team2_speed}-{overtakes}-{laps}"

    # Применяем хэш-функцию MD5 для получения уникального id
    race_id = hashlib.md5(combined_data.encode()).hexdigest()

    return race_id
