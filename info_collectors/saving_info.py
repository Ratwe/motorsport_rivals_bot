import json


def save_to_json(state):
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

    with open("race_data.json", "w") as json_file:
        json.dump(race_data, json_file)
