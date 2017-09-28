import psycopg2
import itertools
from collections import Counter

def checkExtra (players, debug=False):
    c = Counter(elem[1] for elem in players)
    if (debug):
        print('Extracomunitary players:', c[3])
    return (c[3] <= 2)

def checkNational (players, debug=False):
    c = Counter(elem[1] for elem in players)
    if (debug):
        print('National players:', c[1])
    return (c[1] >= 4)

def checkPrize (players, debug=False):
    prize = sum(i for _, _, i in players)
    if (debug):
        print('Total prize:', prize)
    return (prize <= 6500000)

try:
    conn = psycopg2.connect(dbname='supermanager', user='manager', host='sm-pgsql', password='190689')
except:
    print('I am unable to connect to the database.')

cur = conn.cursor()
cur.execute("SELECT player.name, player.nationality_id, player.initial_prize FROM player INNER JOIN custom_position AS pos ON player.custom_pos_id = pos.id WHERE pos.pos_id = 1;")
bases = cur.fetchall()
cur.execute("SELECT player.name, player.nationality_id, player.initial_prize FROM player INNER JOIN custom_position AS pos ON player.custom_pos_id = pos.id WHERE pos.pos_id = 2;")
aleros = cur.fetchall()
cur.execute("SELECT player.name, player.nationality_id, player.initial_prize FROM player INNER JOIN custom_position AS pos ON player.custom_pos_id = pos.id WHERE pos.pos_id = 3;")
pivots = cur.fetchall()

print("Number of bases:", len(bases))
print("Number of aleros:", len(aleros))
print("Number of pivots:", len(pivots))

bases_combi = list(itertools.combinations(bases, 3))
aleros_combi = list(itertools.combinations(aleros, 4))
pivots_combi = list(itertools.combinations(pivots, 4))

print("Number of bases combi:", len(bases_combi))
print("Number of aleros combi:", len(aleros_combi))
print("Number of pivots combi:", len(pivots_combi))
len_total = len(bases_combi)*len(aleros_combi)*len(pivots_combi)
print("Number of total combinations:", len_total)

bases_combi[:] = [tup for tup in bases_combi if checkExtra(tup)]
print("Number of bases combi:", len(bases_combi))
aleros_combi[:] = [tup for tup in aleros_combi if checkExtra(tup)]
print("Number of aleros combi:", len(aleros_combi))
pivots_combi[:] = [tup for tup in pivots_combi if checkExtra(tup)]
print("Number of pivots combi:", len(pivots_combi))

max_prize = 0

for base in bases_combi:
    team = []
    team.extend(base)
    #print(tuple(team))
    if not (checkExtra(tuple(team)) and checkPrize(tuple(team))):
        #print(team)
        continue
    for alero in aleros_combi:
        team.extend(alero)
        if not (checkExtra(tuple(team)) and checkPrize(tuple(team))):
            #print(team)
            team = []
            team.extend(base)
            continue
        for pivot in pivots_combi:
            team.extend(pivot)
            if (checkExtra(tuple(team)) and checkPrize(tuple(team)) and checkNational(tuple(team))):
                prize = prize = sum(i for _, _, i in tuple(team))
                if (prize >= max_prize):
                    print('Max cost possible team found for current iteration:', prize)
                    print(team)
                    max_prize = prize
                team = []
                team.extend(base)
                team.extend(alero)
                break
            team = []
            team.extend(base)
            team.extend(alero)
        team = []
        team.extend(base)