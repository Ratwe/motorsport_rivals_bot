class Lap:
    def __init__(self, lap_data):
        self.lap_number = lap_data['lap_number']
        self.speed_team1 = lap_data['speed_team1']
        self.overtakes_team1 = lap_data['overtakes_team1']
        self.speed_team2 = lap_data['speed_team2']
        self.overtakes_team2 = lap_data['overtakes_team2']
        self.best_lap = lap_data.get('best_lap', False)


class Race:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.score = 0
        self.overtakes_team1 = 0
        self.overtakes_team2 = 0
        self.laps = []

    def add_lap(self, lap_data):
        lap = Lap(lap_data)
        self.laps.append(lap)

    def calculate_score(self):
        for lap in self.laps:
            self.overtakes_team1 += lap.overtakes_team1
            self.overtakes_team2 += lap.overtakes_team2
            if lap.speed_team1 > lap.speed_team2:
                self.score += 1
            elif lap.speed_team2 > lap.speed_team1:
                self.score -= 1

