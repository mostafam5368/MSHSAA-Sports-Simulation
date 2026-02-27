import team, match


with open("/Users/3045368/Library/CloudStorage/GoogleDrive-mostafam5368@parkwayschools.net/My Drive/Endgame/App Dev MSHSAA Coaches/SampleHistory1.csv", "r") as f:
    match_history_a = f.readlines()

with open("/Users/3045368/Library/CloudStorage/GoogleDrive-mostafam5368@parkwayschools.net/My Drive/Endgame/App Dev MSHSAA Coaches/SampleHistory2.csv", "r") as f:
    match_history_b = f.readlines()

# name, record, point diff, strength of schedule, experience rating
team_a = team.Team("Eureka", match_history_a, 1.0, 65.0, 50.0)
team_b = team.Team("Parkway West", match_history_b, 1.0, 65.0, 50.0)

# boosted
game = match.Match(team_a, team_b)

print(f"{team_a}: {team_a.record}")
print(f"{team_b}: {team_b.record}")

print(game)
print(game.display())

