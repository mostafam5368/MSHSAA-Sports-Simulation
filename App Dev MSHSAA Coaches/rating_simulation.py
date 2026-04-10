import team, match, season
import random

eur = team.Team("Eureka")
kir = team.Team("Kirkwood")
lad = team.Team("Ladue")
laf = team.Team("Lafayette")
mar = team.Team("Marquette")
psh = team.Team("Parkway South")
pwh = team.Team("Parkway West")
slu = team.Team("SLUH")

oak = team.Team("Oakville")
fox = team.Team("Fox")
nwe = team.Team("Northwest")
lin = team.Team("Lindbergh")
jac = team.Team("Jackson")
sec = team.Team("Seckman")
via = team.Team("Vianney")
far = team.Team("Farmington")

teams = [eur, kir, lad, laf, mar, psh, pwh, slu, oak, fox, nwe, lin, jac, sec, via, far]
district = season.Season(teams)
district.play_season()

for name in teams:
    print(name.point_diff)
