class Player:
    def __init__(self, name):
        self.name = name

        self.total_score = 0
        self.temp_score = 0

    def hold(self):
        self.total_score += self.temp_score
        self.temp_score = 0

    def increaseTempScore(self, score):
        self.temp_score += score

    def reset_temp_score(self):
        self.temp_score = 0

    def __str__(self):
        return f"{self.name.upper()} - Total: {self.total_score}, Temp: {self.temp_score}"


