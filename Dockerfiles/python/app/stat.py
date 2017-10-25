import os
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime

try:
    conn = psycopg2.connect(dbname='supermanager', user='manager', host='sm-pgsql', password='190689')
except:
    print("I am unable to connect to the database")

cur = conn.cursor()
team_id_dict = {}
player_id_dict = {}
stats_col_dict = {'name': 1, 'time': 2, 't2': 4, 't3': 6, 't1': 8,
    'reb': 11, 'ass': 12, 'br': 13, 'bp': 14, 'tf': 16, 'tc': 17, 'ff': 19, 'fc': 20}


def get_undefined_team_id():
    cur.execute("""SELECT id FROM public.team WHERE name='Undefined team';""")
    return int(cur.fetchone()[0])

undefined_team_id = get_undefined_team_id()
print('Undefined team id:', undefined_team_id)

def real_stats_table(list_tables):
    real_table = list_tables[0]
    for table in list_tables:
        if len(table.find_all('tr')) > len(real_table):
            real_table = table
    return real_table

def get_all_teams_from_db():
    cur.execute("""SELECT id, name FROM public.team ORDER BY id ASC;""")
    return cur.fetchall()

def get_all_players_from_team(team):
    cur.execute("SELECT id, name FROM public.player WHERE team_id = %s ORDER BY id ASC;", (team,))
    return cur.fetchall()

def ask_for_team_id(team):
    list_teams = get_all_teams_from_db()
    for team_db in list_teams:
        if team.lower() == team_db[1].lower():
            print('Found team:', team, 'with id', team_db[0])
            return team_db[0]
    return undefined_team_id

def ask_for_player_id(name, team):
    list_players = get_all_players_from_team(team)
    for player_db in list_players:
        if name.lower() == player_db[1].lower():
            print('Found player:', name, 'with id', player_db[0])
            return player_db[0]
    return -1

def ask_user_for_id(team):
    team_id = undefined_team_id
    list_teams = get_all_teams_from_db()
    for team_db in list_teams:
        print(team_db)
    count = 0
    while count < 3:
        try:
            input_var = int(input('Enter id of team %s: ' % (team)))
        except ValueError:
            print('Invalid input value (must be an integer)')
            count += 1
            continue
        search_team = [item for item in list_teams if item[0] == input_var]
        if search_team:
            db_team = search_team[0]
            count_yn = 0
            while count_yn < 5:
                yn_var = input('Are you sure that id %d (and name %s) belongs to team %s? [y/n] ' % (db_team[0], db_team[1], team))
                if yn_var.lower() == 'y':
                    print('OK')
                    return db_team[0]
                elif yn_var.lower() == 'n':
                    print('KO')
                    break
                else:
                    print('Unexpected character')
                    count_yn += 1
            count +=1
        else:
            print('Id %s not found in database. Try again...' % (input_var))
            count += 1
    print('Fuck you')
    return team_id

def ask_user_for_player_id(name, team):
    player_id = -1
    list_players = get_all_players_from_team(team)
    list_players.append((-1, 'Not a supermanager player'))
    for player_db in list_players:
        print(player_db)
    count = 0
    while count < 3:
        try:
            input_var = int(input('Enter id of player %s: ' % (name)))
        except ValueError:
            print('Invalid input value (must be an integer)')
            count += 1
            continue
        search_team = [item for item in list_players if item[0] == input_var]
        if search_team:
            db_player = search_team[0]
            count_yn = 0
            while count_yn < 5:
                yn_var = input('Are you sure that id %d (and name %s) belongs to player %s? [y/n] ' % (db_player[0], db_player[1], name))
                if yn_var.lower() == 'y':
                    print('OK')
                    return db_player[0]
                elif yn_var.lower() == 'n':
                    print('KO')
                    break
                else:
                    print('Unexpected character')
                    count_yn += 1
            count +=1
        else:
            print('Id %s not found in database. Try again...' % (input_var))
            count += 1
    print('Fuck you')
    return player_id

def check_team(team):
    # Check if key exists on dictionary
    if team in team_id_dict:
        print('Found team in dictionary')
        return team_id_dict[team]
    else:
        # Check with database
        team_id = ask_for_team_id(team)
        if team_id == undefined_team_id:
            print('Need your help')
            final_id = ask_user_for_id(team)
            return final_id
        else:
            return team_id
    return undefined_team_id

def get_player_id(name, team):
    # 1. Check in dictionary
    if name in player_id_dict:
        print('Player %s found at dictionary with id %d' % (name, player_id_dict[name]))
        return player_id_dict[name]
    # 2. Check with database
    player_id = ask_for_player_id(name, team)
    if player_id != -1:
        return player_id
    # 3. Ask for user help
    return ask_user_for_player_id(name, team)

def save_game(game):
    print('Saving game:')
    print(game)
    cur.execute("""INSERT INTO public.game (local_team_id, visiting_team_id, 
        local_points, visiting_points, game_type_id, jornada, date, neutral_court)
        VALUES (%(team_local)s, %(team_visiting)s, %(res_local)s, %(res_visitng)s, %(type)s, 
        %(jornada)s, %(date)s, %(neutral)s) RETURNING id;""", game)
    conn.commit()
    return cur.fetchone()[0]

def get_shots(shots):
    idx = shots.find('/')
    return int(shots[:idx]), int(shots[idx+1:])

def get_rebounds(rebs):
    idx = rebs.find('+')
    return int(rebs[:idx]), int(rebs[idx+1:])

def save_stat(stats):
    cur.execute("""INSERT INTO public.stats (game_id, player_id, total_time, t2a, 
    t2i, t3a, t3i, t1a, t1i, rd, ro, ass, br, bp, tf, tc, ff, fc)
	VALUES (%(game)s, %(id)s, %(time)s, %(t2a)s, %(t2i)s, %(t3a)s, 
    %(t3i)s, %(t1a)s, %(t1i)s, %(rd)s, %(ro)s, %(ass)s, %(br)s, %(bp)s, %(tf)s, %(tc)s, %(ff)s, %(fc)s) RETURNING id;""", stats)
    conn.commit()
    return cur.fetchone()[0]

directory = os.fsencode('stats')

for file in os.listdir(directory):
    with open('stats/' + os.fsdecode(file)) as fp:
        first_team = True
        game = {}
        game['team_local'] = undefined_team_id
        game['team_visiting'] = undefined_team_id
        game['type'] = 3 # Amistoso
        game['neutral'] = True
        soup = BeautifulSoup(fp, 'html.parser')
        game_data = soup.find_all('tr', class_='estnegro')[0]
        game_info = game_data.find_all('td')[0].string
        game_info = game_info.replace(' ', '').split('|')
        jornada_idx = game_info[0].find('J')
        game['jornada'] = game_info[0][jornada_idx+1:]
        date = datetime.strptime(game_info[1], '%d/%m/%Y')
        game['date'] = date.isoformat()    
        stats_table = soup.find_all('table', class_='estadisticasnew')
        stats_table = real_stats_table(stats_table)
        rows = stats_table.find_all('tr')
        for row in rows:
            if not row.find('td', class_='estverdel'):
                continue
            # New team stat
            new_team = row.find('td', class_='estverdel').string
            idx = new_team.rfind(' ')
            team = new_team[:idx]
            result = new_team[idx+1:]
            print('New team:', new_team[:idx], 'Result:', new_team[idx+1:])
            team_id = check_team(team)
            # Save team in dictionary
            if team_id != undefined_team_id:
                team_id_dict[team] = team_id
            if first_team:
                game['team_local'] = team_id
                game['res_local'] = result
                first_team = False
            else:
                game['team_visiting'] = team_id
                game['res_visitng'] = result
        game_id = save_game(game)
        first_team = True
        team_id = game['team_local']
        for row in rows:
            if row.find('td', class_='estverdel'):
                if first_team:
                    first_team = False
                else:
                    team_id = game['team_visiting']
                continue
            if team_id == undefined_team_id or team_id == 2 or team_id == 10:
                continue
            columns = row.find_all('td')
            if len(columns) > 20 and columns[1].find('a'):
                if columns[2].string != u'\xa0':
                    # Player played
                    player = {}
                    player['game'] = game_id
                    player_name = columns[stats_col_dict['name']].find('a').string
                    player_id = get_player_id(player_name, team_id)
                    player_id_dict[player_name] = player_id
                    if player_id == -1:
                        continue
                    player['id'] = player_id
                    # Get stats of the player
                    time_played = columns[stats_col_dict['time']].string
                    time_idx = time_played.find(':')
                    player['time'] = int(time_played)*60 if time_idx == -1 else (int(time_played[:time_idx])*60 + int(time_played[time_idx + 1:]))
                    shot2 = get_shots(columns[stats_col_dict['t2']].string)
                    shot3 = get_shots(columns[stats_col_dict['t3']].string)
                    shot1 = get_shots(columns[stats_col_dict['t1']].string)
                    player['t2a'] = shot2[0]
                    player['t2i'] = shot2[1]
                    player['t3a'] = shot3[0]
                    player['t3i'] = shot3[1]
                    player['t1a'] = shot1[0]
                    player['t1i'] = shot1[1]
                    reb = get_rebounds(columns[stats_col_dict['reb']].string)
                    player['rd'] = reb[0]
                    player['ro'] = reb[1]
                    player['ass'] = columns[stats_col_dict['ass']].string
                    player['br'] = columns[stats_col_dict['br']].string
                    player['bp'] = columns[stats_col_dict['bp']].string
                    player['tf'] = columns[stats_col_dict['tf']].string
                    player['tc'] = columns[stats_col_dict['tc']].string
                    player['ff'] = columns[stats_col_dict['ff']].string
                    player['fc'] = columns[stats_col_dict['fc']].string
                    save_stat(player)