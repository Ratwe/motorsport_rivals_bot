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
                self.scores[0] += 1
            elif lap.speed_team2 > lap.speed_team1:
                self.scores[1] += 1

    def print_info(self):
        print(f"team1 = {self.team1}")
        print(f"team2 = {self.team2}")
        print(f"overtakes_team1 = {self.overtakes_team1}")
        print(f"overtakes_team2 = {self.overtakes_team2}")
        print(f"scores = {self.scores[0]} : {self.scores[1]}")

        for lap in self.laps:
            print(f"lap #{lap.number}: ")
            print(f"speed_team1 = {lap.speed_team1}")
            print(f"speed_team2 = {lap.speed_team2}")
            print(f"best_lap = {lap.best_lap}\n")

