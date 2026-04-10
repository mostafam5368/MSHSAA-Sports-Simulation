import team
import math
import random

class Match:
    """This class represents a match between a Home and Away team."""

    max_home_boost = 0.02
    max_momentum_boost = 0.05

    def __init__(self, a:team.Team, b:team.Team, is_neutral:bool = False, boosted:bool = True):
        self.home = a
        self.away = b

        # store probabilites
        self.home_probability = self.home.probability_of_beating(self.away)
        self.away_probability = self.away.probability_of_beating(self.home)

        self.is_neutral = is_neutral

        # apply home and momentum boosts
        if boosted:
            self.apply_boosts()

        self.match_result = None

    def apply_boosts(self):
        if not self.is_neutral:
            self.apply_home_boost()
        
        self.apply_momentum_boost()

    def apply_home_boost(self):
        home_boost = self.home_boost()

        self.home_probability += home_boost
        self.away_probability -= home_boost

    def apply_momentum_boost(self):
        momentum_boost = self.momentum_boost()

        if (self.home.win_streak() > self.away.win_streak()):
            self.home_probability += momentum_boost
            self.away_probability -= momentum_boost
        else:
            self.home_probability -= momentum_boost
            self.away_probability += momentum_boost

    def home_boost(self):
        win_pct_at_home = self.home.home_win_pct()

        if win_pct_at_home > .50:
            return self.max_home_boost
        else:
            return 0

    def momentum_boost(self):
        streak_threshold = 3

        # calculate difference in win streak only if both teams have a win streak of at least 3 
        if (self.home.win_streak() > streak_threshold) and (self.away.win_streak() > streak_threshold):
            momentum_diff = abs(self.home.win_streak() - self.away.win_streak())
        else:
            momentum_diff = max(self.home.win_streak(), self.away.win_streak())

        # a win streak is only considered after passing the threshold
        if momentum_diff < streak_threshold:
            return 0.0

        boost = (self.max_momentum_boost) * (1 - 2.718 ** (-0.45 * (momentum_diff - (streak_threshold - 1)))) # AI

        return boost
       
    def get_poisson_score(self, lam):
        L = math.exp(-lam)
        k = 0
        p = 1.0
        while p > L:
            k += 1
            p *= random.random()
        return k - 1
    
    # return (winning team, losing team, score)
    def result(self, league_avg=1.57):
        # Instead of finding the mode of 10 games, simulate ONE actual game
        
        # Calculate lambda based on current team stats
        
        h_exp = max(0.01, league_avg * self.home_probability * 2.0)
        a_exp = max(0.01, league_avg * self.away_probability * 2.0)
        

        # Generate one random score from the Poisson distribution
        home_score = self.get_poisson_score(h_exp)
        away_score = self.get_poisson_score(a_exp)
        score = (home_score, away_score)

        if score[0] > score[1]:
            return self.home, self.away, score
        elif score[0] < score[1]:
            return self.away, self.home, score
        else:
            return "DRAW"
        
    def play_match(self):
        self.match_result = self.result()

        # update record and point difference
        if self.match_result != "DRAW":
            self.match_result[0].record[0] += 1
            self.match_result[1].record[1] += 1

            # goals scored - goals conceded
            score_diff = abs(self.match_result[2][0] - self.match_result[2][1])

            self.match_result[0].point_diff += score_diff
            self.match_result[1].point_diff -= score_diff
        elif self.match_result == "DRAW":
            self.home.record[2] += 1
            self.away.record[2] += 1

        # update win percentage
        self.home.win_pct = self.home.calculate_win_pct()
        self.away.win_pct = self.away.calculate_win_pct()

        # update ratings
        self.home.rating = self.home.calculate_rating()
        self.away.rating = self.away.calculate_rating()

    def __repr__(self):
        return f"{self.away} @ {self.home}"

    def __str__(self):
        probabilities = f"{round(self.home_probability * 100, 2)}%\t\t\t   {round(self.away_probability * 100, 2)}%"

        max_bars = 32
        num_bars = int(max_bars * (self.home_probability))
        percentage_bar = "-"*num_bars + "/" + "-"*(max_bars - num_bars)
        
        return f"{self.away} @ {self.home}\n{probabilities}\n{percentage_bar}"
    