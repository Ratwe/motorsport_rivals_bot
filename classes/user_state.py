from classes.race import Race


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
