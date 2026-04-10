import random

class Team:
    """This class represents a sports team."""

    # NEW WAY
    def __init__(self, name:str, schedule:list=None):
        self.name = name

        if schedule == None:
            self.schedule = []
        else:
            self.schedule = schedule
        
        self.match_history = []

        self.record = [0, 0, 0]
        self.win_pct = 0.0

        self.point_diff = 0.0

        self.strength_of_schedule = random.randint(40, 70) / 100.0
        self.experience_rating = random.randint(40, 70) / 100.0

        self.rating = self.calculate_rating()

    # rating 
    def calculate_rating(self):
        # win percentage, point difference, strength of schedule, team experience
        weight_scheme = [.40, .20, .30, .10]

        raw_point_diff = (self.point_diff + 50.0) / 100.0
        normalized_point_diff = max(0.0, min(1.0, raw_point_diff))

        metrics = [self.win_pct, normalized_point_diff, self.strength_of_schedule, self.experience_rating]
        
        total = 0
        for i in range(len(metrics)):
            total += metrics[i] * weight_scheme[i]

        # from readme
        rating = total * 100.0
        return rating

    def win_streak(self):
        streak = 0

        for game in reversed(self.match_history):
            if (game.match_result[0] == self):
                streak += 1
            else:
                break
        
        return streak

    # chance of beating another team
    def probability_of_beating(self, other_team, variance=30.0):
        rating_diff = self.rating - other_team.rating

        # from ai
        probability = 1 / (1 + 10 ** (-rating_diff / variance))
        return probability
    
    def calculate_win_pct(self, conditions:dict=None):
        record = self.record

        games = sum(record)

        if games == 0:
          return 0.0

        return (record[0] + (0.5 * record[2])) / games
    
    def home_win_pct(self):
        record = [0, 0, 0]

        for game in self.match_history:
            if game.home == self and game.match_result != None:
                if game.match_result == "DRAW":
                    record[2] += 1
                elif game.match_result[0] == self:
                    record[0] += 1
                else:
                    record[1] += 1

        games = sum(record)

        if games == 0:
          return 0.0

        return (record[0] + (0.5 * record[2])) / games
    
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name