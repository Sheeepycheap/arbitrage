from bs4 import BeautifulSoup
import requests

competition_urls = {
		'football':
		{
			"ligue1": "https://www.betclic.fr/football-s1/ligue-1-uber-eats-c4",
			"liga": "https://www.betclic.fr/football-s1/espagne-liga-primera-c7",
			"bundesliga": "https://www.betclic.fr/football-s1/allemagne-bundesliga-c5",
			"premier-league": "https://www.betclic.fr/football-s1/angl-premier-league-c3",
			"serie-a": "https://www.betclic.fr/football-s1/italie-serie-a-c6",
			"primeira": "https://www.betclic.fr/football-s1/portugal-primeira-liga-c32",
			"serie-a-brasil": "https://www.betclic.fr/football-s1/bresil-serie-a-c187",
			"a-league": "https://www.betclic.fr/football-s1/australie-a-league-c1874",
			"bundesliga-austria": "https://www.betclic.fr/football-s1/autriche-bundesliga-c35",
			"division-1a": "https://www.betclic.fr/football-s1/belgique-division-1a-c26",
			"super-lig": "https://www.betclic.fr/football-s1/turquie-super-lig-c37",
		},
		'basketball':
		{
			"nba": "https://www.betclic.fr/basket-ball-s4/nba-c13",
			"euroleague": "https://www.betclic.fr/basket-ball-s4/euroligue-c14",
		}
}

def get_page(competition):
	if (competition["sport"] in competition_urls and competition["competition"] in competition_urls[competition["sport"]]):
		url = competition_urls[competition["sport"]][competition["competition"]]
	else:
		print("Url not in list.")
		return None
	response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
	html = BeautifulSoup(response.content, 'html.parser')
	return html

def get_games(competition):
	html = get_page(competition)
	games = []
	game_elements = html.select(".groupEvents_card")
	for el in game_elements:
		names = el.select(".scoreboard_contestantLabel")
		team1 = "".join(names[0].text.split())
		team2 = "".join(names[1].text.split())
		odd_els = el.select(".oddValue")
		odds = []
		for odd_el in odd_els[:3]:
			try :
				odds.append(float(odd_el.text.replace(",", ".")))
			except :
				continue
		games.append({
			'team1': team1,
			'team2': team2,
			'odds': odds
		})
	return games

# maintenant on souhaite manipuler des dataframes : 
# maintenant on souhaite manipuler des dataframes : 
import pandas as pd 
import numpy as np 
def into_a_pd(competition):
    key = []
    games = get_games(competition=competition)
    team1 = []
    team2 = []
    odd1 = []
    odd2 = []
    oddnul = []
	
    if competition['sport'] == 'football' :
        for i in range(0,len(games)) :
            try : 
                odd2.append(games[i]['odds'][2]) 
                team1.append(games[i]['team1'])
                team2.append(games[i]['team2'])
                odd1.append(games[i]['odds'][0])
                oddnul.append(games[i]['odds'][1])
                key.append(games[i]['team1'] + "v" + games[i]['team2'])
            except :
                continue
        data = {
                'team1' : team1,
                'team2' : team2,
                'odd of team 1 winning' : odd1,
                'odds of equality ': oddnul,
                'odd of team 2 winning' : odd2,
				'key' : key
            }
            
    else :
        for i in range(len(games)) :
            key.append(games[i]['team1'] + "v" + games[i]['team2'])
            team1.append(games[i]['team1'])
            team2.append(games[i]['team2'])
            odd1.append(games[i]['odds'][0])
            odd2.append(games[i]['odds'][1])
        data = {
                'team1' : team1,
                'team2' : team2,
                'odd of team 1 winning' : odd1,
                'odd of team 2 winning' : odd2,
				'key' : key
            }
   

    df = pd.DataFrame(data=data)
    return df 

