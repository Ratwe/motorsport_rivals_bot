import hashlib


class Lap:
    def __init__(self, lap_data):
        self.number = lap_data['lap_number']
        self.speed_team1 = lap_data['speed_team1']
        self.speed_team2 = lap_data['speed_team2']
        self.best_lap = lap_data['best_lap']


class Race:
    race_id = None
    team1 = None
    team2 = None
    scores = [0, 0]
    overtakes_team1 = 0
    overtakes_team2 = 0
    speed_team1 = 0
    speed_team2 = 0
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
        self.scores = [0, 0]
        for lap in self.laps:
            if lap.speed_team1 > lap.speed_team2:
                self.scores[0] += int(lap.best_lap)
            elif lap.speed_team2 > lap.speed_team1:
                self.scores[1] += int(lap.best_lap)

    def calculate_speed(self):
        for lap in self.laps:
            self.speed_team1 += lap.speed_team1
            self.speed_team2 += lap.speed_team2

    def calculate_race_id(self):
        # Объединяем скорости команд и характеристики гонки
        combined_data = f"{self.speed_team1}-{self.speed_team2}"

        # Применяем хэш-функцию MD5 для получения уникального id
        self.race_id = hashlib.md5(combined_data.encode()).hexdigest()

    def get_info_as_text(self, full=False):
        info = "Информация о гонке:\n\n"

        if self.race_id is not None:
            info += f"race_id = {self.race_id}\n"
        if self.team1 is not None:
            info += f"team1 = {self.team1}\n"
        if self.team2 is not None:
            info += f"team2 = {self.team2}\n"

        info += f"speed_team1 = {self.speed_team1}\n"
        info += f"speed_team2 = {self.speed_team2}\n"
        info += f"overtakes_team1 = {self.overtakes_team1}\n"
        info += f"overtakes_team2 = {self.overtakes_team2}\n"
        info += f"scores = {self.scores[0]} : {self.scores[1]}\n\n"

        if full:
            for lap in self.laps:
                info += f"lap #{lap.number}:\n"
                info += f"speed_team1 = {lap.speed_team1}\n"
                info += f"speed_team2 = {lap.speed_team2}\n"
                info += f"best_lap = {lap.best_lap}\n\n"

        return info

    def print_info(self):
        print(self.get_info_as_text())
