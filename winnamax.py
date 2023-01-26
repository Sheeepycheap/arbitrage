import requests
import json

competition_urls = {
	'football':
	{
		"ligue1": "https://www.winamax.fr/paris-sportifs/sports/1/7/4",
		"liga": "https://www.winamax.fr/paris-sportifs/sports/1/32/36",
		"bundesliga": "https://www.winamax.fr/paris-sportifs/sports/1/30/42",
		"premier-league": "https://www.winamax.fr/paris-sportifs/sports/1/1/1",
		"serie-a": "https://www.winamax.fr/paris-sportifs/sports/1/31/33",
		"primeira": "https://www.winamax.fr/paris-sportifs/sports/1/44/52",
		"serie-a-brasil": "https://www.winamax.fr/paris-sportifs/sports/1/13/83",
		"a-league": "https://www.winamax.fr/paris-sportifs/sports/1/34/144",
		"bundesliga-austria": "https://www.winamax.fr/paris-sportifs/sports/1/17/29",
		"division-1a": "https://www.winamax.fr/paris-sportifs/sports/1/33/38",
		"super-lig": "https://www.winamax.fr/paris-sportifs/sports/1/46/62",
	},
	'basketball':
	{
		"nba": "https://www.winamax.fr/paris-sportifs/sports/2/800000076/177",
		"euroleague": "https://www.winamax.fr/paris-sportifs/sports/2/800000034/153",
	}
}

def get_page(competition):
	if (competition["sport"] in competition_urls and competition["competition"] in competition_urls[competition["sport"]]):
		url = competition_urls[competition["sport"]][competition["competition"]]
	else:
		print("Url not in list.")
		return None
	response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
	html = response.text
	return html

def get_json(competition):
	html = get_page(competition)
	split1 = html.split("var PRELOADED_STATE = ")[1]
	split2 = split1.split(";</script>")[0]
	return json.loads(split2)

def get_id(competition):
	url = competition_urls[competition["sport"]][competition["competition"]]
	return int(url.split("/")[-1])

def get_games(competition):
	games = []
	json = get_json(competition)
	for game in json['matches']:
		if (json['matches'][game]['tournamentId'] != get_id(competition)):
			continue
		if (json['matches'][game]['competitor1Name'] is None or json['matches'][game]['competitor2Name'] is None) :
			continue
		team1 = "".join(json['matches'][game]['competitor1Name'].split())
		team2 = "".join(json['matches'][game]['competitor2Name'].split())
		bet_id = json['matches'][game]['mainBetId']
		bet = json['bets'][str(bet_id)]['outcomes']
		if (competition["sport"] == "football" and len(bet) != 3):
			continue
		if (competition["competition"] == "basketball" and len(bet) != 2):
			continue
		if (competition["sport"] == "football"):
			odds = [
				json['odds'][str(bet[0])],
				json['odds'][str(bet[1])],
				json['odds'][str(bet[2])],
			]
		elif (competition["sport"] == "basketball"):
			odds = [
				json['odds'][str(bet[0])],
				json['odds'][str(bet[1])],
			]
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

