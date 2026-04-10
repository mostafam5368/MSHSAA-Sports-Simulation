import match, team
import random
import time

class Season:
    def __init__(self, teams:list[team.Team], day=0):
        self.teams = teams
        self.day = 0
        self.gen_schedules()

    def gen_schedules(self):
        num_teams = len(self.teams)
        num_rounds = num_teams - 1
        half_size = num_teams // 2

        # Create a working list to rotate teams around
        rotating_teams = self.teams

        for round_num in range(num_rounds):
            # Pair up teams: first with last, second with second-to-last, etc.
            for i in range(half_size):
                team1 = rotating_teams[i]
                team2 = rotating_teams[num_teams - 1 - i]

                # Populate each team's schedule list
                if team1.name != "BYE" and team2.name != "BYE":
                    team1.schedule.append(team2)
                    team2.schedule.append(team1)

            # The Circle Rotation: Keep index 0 fixed, rotate the rest clockwise
            rotating_teams.insert(1, rotating_teams.pop())
    
    # WIP
    def forward(self):
        already_played = []

        for t in self.teams:
            if t not in already_played:
                opponent = t.schedule[self.day]
                home_or_away = random.random()

                if home_or_away < 0.5:
                    new_match = match.Match(t, opponent)
                else:
                    new_match = match.Match(opponent, t)
                    
                t.match_history.append(new_match)
                opponent.match_history.append(new_match)
                
                new_match.play_match()
                already_played.append(opponent)
  
        self.day += 1

    def play_season(self, first_day=0):
        for first_day in range(len(self.teams) - 1):
            print(f"Matchday {self.day + 1}")
            self.forward()

            print()

        for t in self.teams:
            print(f"{t.name} / {t.record} / {int(t.rating)}")

    def __str__(self):
        return f"Matchday {self.day + 1}"
