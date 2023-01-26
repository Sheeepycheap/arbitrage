from bs4 import BeautifulSoup
import requests

competition_urls = {
	'football':
	{
		"ligue1": "https://paris-sportifs.pmu.fr/pari/competition/169/football/ligue-1-conforama",
		"liga": "https://paris-sportifs.pmu.fr/pari/competition/322/football/la-liga",
		"bundesliga": "https://paris-sportifs.pmu.fr/pari/competition/32/football/bundesliga",
		"premier-league": "https://paris-sportifs.pmu.fr/pari/competition/13/football/premier-league",
		"serie-a": "https://paris-sportifs.pmu.fr/pari/competition/308/football/italie-serie-a",
		"primeira": "https://paris-sportifs.pmu.fr/pari/competition/273/football/primeira-liga",
		"serie-a-brasil": "https://paris-sportifs.pmu.fr/pari/competition/1779/football/s%C3%A9rie",
		"a-league": "https://paris-sportifs.pmu.fr/pari/competition/1812/football/australie-league",
		"bundesliga-austria": "https://paris-sportifs.pmu.fr/pari/competition/63/football/autriche-bundesliga",
		"division-1a": "https://paris-sportifs.pmu.fr/pari/competition/8124/football/division-1a",
		"super-lig": "https://paris-sportifs.pmu.fr/pari/competition/1529/football/turquie-super-ligue",
	},
	'basketball':
	{
		"nba": "https://paris-sportifs.pmu.fr/pari/competition/3502/basket-us/nba",
		"euroleague": "https://paris-sportifs.pmu.fr/pari/competition/1402/basket-euro/euroligue-h"
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
	game_elements = html.select(".pmu-event-list-grid-highlights-formatter-row")
	for el in game_elements:
		game_name = el.select(".trow--event--name")[0].text
		game_name = "".join(game_name.split())
		team1, team2 = game_name.split("//")
		odds_el = el.select(".hierarchy-outcome-price")
		odds = []
		for el2 in odds_el:
			try :
				tmp = "".join(el2.text.split()).replace(",", ".")
				odds.append(float(tmp))
			except :
				continue
		games.append({
			'team1': team1,
			'team2': team2,
			'odds': odds
		})
	return games


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