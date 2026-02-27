class Team:
    """This class represents a sports team."""

    def __init__(self, name:str, match_history, point_diff:float, strength_of_schedule:float, experience_rating:float):
        self.name = name
        self.match_history = match_history
        self.result_history = self.process_history(match_history)
        self.record = [self.result_history.count("win"), self.result_history.count("loss"), self.result_history.count("draw")]

        # from readme
        self.win_pct = self.calculate_win_pct()

        # normalized (from ai)
        self.point_diff = (point_diff + 10.0) / 20.0

        self.strength_of_schedule = strength_of_schedule / 100.0
        self.experience_rating = experience_rating / 100.0

        self.rating = self.calculate_rating()

    def process_history(self, history) -> list:
        output = []

        for match in history:
            output.append(match.split(",")[2])

        return output
    
    # rating 
    def calculate_rating(self):
        # from readme
        # win percentage, point difference, strength of schedule, team experience
        weight_scheme = [.40, .20, .30, .10]
        # alt_weight_scheme = []

        metrics = [self.win_pct, self.point_diff, self.strength_of_schedule, self.experience_rating]
        
        total = 0
        for i in range(len(metrics)):
            total += metrics[i] * weight_scheme[i]

        # from readme
        rating = total * 100.0
        return rating
    
    def get_win_streak(self):
        win_streak = 0

        for element in reversed(self.result_history):
            if (element == "win"):
                win_streak += 1
            else:
                break
        
        return win_streak

    # chance of beating another team
    def probability_of_beating(self, other_team):
        rating_diff = self.rating - other_team.rating

        # from ai
        probability = 1 / (1 + 10 ** (-rating_diff / 30.0))
        return probability
    
    def calculate_win_pct(self, conditions:dict=None):
        record = self.record

        if conditions != None:
            record = [0, 0, 0]

            for line in self.match_history:
                match = line.strip().split(",")
                flag = True

                for (k, v) in conditions.items():
                    if match[v] != k:
                        flag = False
                        break

                if flag:
                    if match[2] == "win":
                        record[0] += 1
                    elif match[2] == "draw":
                        record[2] += 1
                    else:
                        record[1] += 1

        print(record)
        games = sum(record)

        #if games == 0:
        #   return 0.5

        return (record[0] + (0.5 * record[2])) / games

    # determines if the other team is a rival
    def is_rival(self, other_team) -> bool:
        return True
    
    def __str__(self):
        return self.name