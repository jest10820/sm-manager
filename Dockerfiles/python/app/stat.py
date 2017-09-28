from bs4 import BeautifulSoup
import psycopg2

try:
    conn = psycopg2.connect(dbname='supermanager', user='manager', host='sm-pgsql', password='190689')
except:
    print("I am unable to connect to the database")

cur = conn.cursor()
team_id_dict = {}
player_id_dict = {}

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
    print(team)
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

with open('stat_1.html') as fp:
    first_team = True
    soup = BeautifulSoup(fp, 'html.parser')
    stats_table = soup.find_all('table', class_='estadisticasnew')
    stats_table = real_stats_table(stats_table)
    rows = stats_table.find_all('tr')
    for row in rows:
        if row.find('td', class_='estverdel'):
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
        elif not row.find('td', class_='estverde'):
            columns = row.find_all('td')
            if len(columns) > 20 and columns[1].find('a'):
                if columns[2].string != u'\xa0':
                    # Player played
                    player = {}
                    player_name = columns[1].find('a').string
                    player_id = get_player_id(player_name, team_id)
                    if player_id == -1:
                        continue
                    else:
                        print(player_id, player_name)
                        print(team, team_id)
                else:
                    print('0 minuts')
                try:
                    print(int(columns[3].string))
                except ValueError:
                    print('Didn\'t play')