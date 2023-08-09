class UserState:
    def __init__(self):
        self.entering_race_info = False
        self.entering_team1 = False
        self.entering_team2 = False
        self.entering_overtakes1 = False
        self.entering_overtakes2 = False
        self.race = Race(None, None, None, None)
        self.printing_info = False

    def print_info(self):
        print(f"entering_race_info = {self.entering_race_info}")
        print(f"entering_team1 = {self.entering_team1}")
        print(f"entering_team2 = {self.entering_team2}")
        print(f"entering_overtakes1 = {self.entering_overtakes1}")
        print(f"entering_overtakes2 = {self.entering_overtakes2}")
        print(f"printing_info = {self.printing_info}")


class Lap:
    def __init__(self, lap_data):
        self.number = lap_data['lap_number']
        self.speed_team1 = lap_data['speed_team1']
        self.speed_team2 = lap_data['speed_team2']
        self.best_lap = lap_data['best_lap']


class Race:
    team1 = None
    team2 = None
    scores = [0, 0]
    overtakes_team1 = 0
    overtakes_team2 = 0
    laps = []

    def __init__(self, team1, team2, overtakes_team1, overtakes_team2):
        self.team1 = team1
        self.team2 = team2
        self.overtakes_team1 = overtakes_team1
        self.overtakes_team2 = overtakes_team2

    def add_lap(self, lap_data):
        lap = Lap(lap_data)
        self.laps.append(lap)

    def calculate_score(self):
        for lap in self.laps:
            if lap.speed_team1 > lap.speed_team2:
                self.scores[0] += lap.best_lap
            elif lap.speed_team2 > lap.speed_team1:
                self.scores[1] += lap.best_lap

    def get_info_as_text(self):
        info = "Информация о гонке:\n\n"
        info += f"team1 = {self.team1}\n"
        info += f"team2 = {self.team2}\n"
        info += f"overtakes_team1 = {self.overtakes_team1}\n"
        info += f"overtakes_team2 = {self.overtakes_team2}\n"
        info += f"scores = {self.scores[0]} : {self.scores[1]}\n"

        for lap in self.laps:
            info += f"lap #{lap.number}:\n"
            info += f"speed_team1 = {lap.speed_team1}\n"
            info += f"speed_team2 = {lap.speed_team2}\n"
            info += f"best_lap = {lap.best_lap}\n\n"

        return info

    def print_info(self):
        print(self.get_info_as_text())

