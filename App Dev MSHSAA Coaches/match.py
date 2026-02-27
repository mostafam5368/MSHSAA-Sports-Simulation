import team

class Match:
    """This class represents a match between a Home and Away team."""

    max_home_boost = 0.02
    max_momentum_boost = 0.05

    def __init__(self, a:team, b:team, is_neutral:bool = False, boosted:bool = True):
        self.home = a
        self.away = b

        # store probabilites
        self.home_probability = self.home.probability_of_beating(self.away)
        self.away_probability = self.away.probability_of_beating(self.home)

        self.is_neutral = is_neutral

        # apply home and momentum boosts
        if boosted:
            self.apply_boosts()

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

        if (self.home.get_win_streak() > self.away.get_win_streak()):
            self.home_probability += momentum_boost
            self.away_probability -= momentum_boost
        else:
            self.home_probability -= momentum_boost
            self.away_probability += momentum_boost

    def home_boost(self):
        win_pct_at_home = self.home.calculate_win_pct({"home":2})

        if win_pct_at_home > .50:
            return self.max_home_boost
        else:
            return 0

    def momentum_boost(self):
        streak_threshold = 3

        # calculate difference in win streak only if both teams have a win streak of at least 3 
        if (self.home.get_win_streak() > streak_threshold) and (self.away.get_win_streak() > streak_threshold):
            momentum_diff = abs(self.home.get_win_streak() - self.away.get_win_streak())
        else:
            momentum_diff = max(self.home.get_win_streak(), self.away.get_win_streak())

        # a win streak is only considered after passing the threshold
        if momentum_diff < streak_threshold:
            return 0.0

        boost = (self.max_momentum_boost) * (1 - 2.718 ** (-0.45 * (momentum_diff - (streak_threshold - 1)))) # AI

        return boost

    def display(self):
        probabilities = f"{round(self.home_probability * 100, 2)}%\t\t\t   {round(self.away_probability * 100, 2)}%"

        max_bars = 32
        num_bars = int(max_bars * (self.home_probability))
        percentage_bar = "-"*num_bars + "/" + "-"*(max_bars - num_bars)
        
        return f"{probabilities}\n{percentage_bar}"
    
    def __str__(self):
        return f"{self.away} @ {self.home}"
    