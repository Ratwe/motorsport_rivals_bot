from classes.race import Race


def calc_average_race(races_list):
    count = len(races_list)
    avg_race = Race(None, None, 0, 0)

    if count >= 1:
        avg_race = races_list[0]
        avg_race.race_id = None
        avg_race.team1 = None
        avg_race.team2 = None

    for race in races_list[1:]:
        avg_race.scores[0] += race.scores[0]
        avg_race.scores[1] += race.scores[1]

        avg_race.overtakes_team1 += race.overtakes_team1
        avg_race.overtakes_team2 += race.overtakes_team2

        avg_race.speed_team1 += race.speed_team1
        avg_race.speed_team2 += race.speed_team2

        avg_laps = avg_race.laps.copy()

        for lap in race.laps:
            lap_num = int(lap.number) - 1
            avg_laps[lap_num].speed_team1 += lap.speed_team1
            avg_laps[lap_num].speed_team2 += lap.speed_team2
            avg_laps[lap_num].best_lap += lap.best_lap

    avg_race.scores[0] /= count
    avg_race.scores[1] /= count
    avg_race.overtakes_team1 /= count
    avg_race.overtakes_team2 /= count
    avg_race.speed_team1 /= count
    avg_race.speed_team2 /= count

    for avg_lap in avg_race.laps:
        avg_lap.speed_team1 /= count
        avg_lap.speed_team2 /= count
        avg_lap.best_lap /= count

    return avg_race