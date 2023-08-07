class UserState:
    def __init__(self):
        self.entering_club = False
        self.entering_teams = False
        self.entering_overtakes = False


class Lap:
    def __init__(self, lap_data):
        self.number = lap_data['lap_number']
        self.speed_team1 = lap_data['speed_team1']
        self.speed_team2 = lap_data['speed_team2']
        self.best_lap = lap_data.get('best_lap', False)


class Race:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.scores = [0, 0]
        self.overtakes_team1 = 0
        self.overtakes_team2 = 0
        self.laps = []

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

