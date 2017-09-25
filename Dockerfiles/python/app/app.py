from bs4 import BeautifulSoup

custom_pos_id = {'posicion1': 1, 'posicion3': 2, 'posicion5': 3}
team_id = {
'Real Madrid': 12, 'Unicaja': 16, 'Baskonia': 1, 'FC Barcelona Lassa': 3,
'Herbalife Gran Canaria': 5, 'San Pablo Burgos': 14, 'Valencia Basket Club': 18,
'MoraBanc Andorra': 9, 'Real Betis Energía Plus': 11, 'Gipuzkoa Basket Club': 4,
'Monbus Obradoiro': 7, 'Tecnyconta Zaragoza': 15, 'UCAM Murcia CB': 17,
'RETAbet Bilbao Basket': 13, 'Iberostar Tenerife': 6, 'Montakit Fuenlabrada': 8
}

with open('mercado.html') as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    div = soup.find(id='contentmercado')
    tables = div.find_all('table', class_='listajugadores')
    for table in tables:
        body = table.find('tbody')
        for tr in body.find_all('tr'):
            team_row = tr.find('td', class_='equipo')
            team = team_row.find('img')
            player = tr.find('td', class_='jugador')
            #print(player.string)
            #print(team_id[team['title']])
