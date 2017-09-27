from bs4 import BeautifulSoup
import psycopg2

try:
    conn = psycopg2.connect(dbname='supermanager', user='manager', host='sm-pgsql', password='190689')
except:
    print("I am unable to connect to the database")

cur = conn.cursor()

custom_pos_id = {'posicion1': 1, 'posicion3': 2, 'posicion5': 3}
team_id = {
'Real Madrid': 12, 'Unicaja': 16, 'Baskonia': 1, 'FC Barcelona Lassa': 3,
'Herbalife Gran Canaria': 5, 'San Pablo Burgos': 14, 'Valencia Basket Club': 18,
'MoraBanc Andorra': 9, 'Real Betis Energía Plus': 11, 'Gipuzkoa Basket Club': 4,
'Monbus Obradoiro': 7, 'Tecnyconta Zaragoza': 15, 'UCAM Murcia CB': 17,
'RETAbet Bilbao Basket': 13, 'Iberostar Tenerife': 6, 'Montakit Fuenlabrada': 8
}
nationality_id = {'Español': 1, 'Europeo': 2, 'Extracomunitario': 3}

def get_nationality(td):
    nation = 'Europeo'
    for item in td.find_all('img'):
        if item['title'] == 'Español' or item['title'] == 'Extracomunitario':
            return item['title']
    return nation

with open('mercado.html') as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    div = soup.find(id='contentmercado')
    tables = div.find_all('table', class_='listajugadores')
    for table in tables:
        body = table.find('tbody')
        for tr in body.find_all('tr'):
            player = {}
            player['pos'] = custom_pos_id[table['id']]
            team_row = tr.find('td', class_='equipo')
            team = team_row.find('img')
            player['team'] = team_id[team['title']]
            player_name = tr.find('td', class_='jugador')
            player['name'] = player_name.string
            prize_row = tr.find('td', class_='precio')
            prize = prize_row.find('span').string
            player['prize'] = int(prize.replace('.', ''))
            player['nation'] = nationality_id[get_nationality(tr.find('td', class_='iconos'))]
            print(player)
            cur.execute("""INSERT INTO public.player (initial_prize, custom_pos_id, name, nationality_id, team_id)
                VALUES (%(prize)s, %(pos)s, %(name)s, %(nation)s, %(team)s);""", player)

conn.commit()
conn.close()
            
