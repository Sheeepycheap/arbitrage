import arb
import log

log.init()

competition = [
    {'sport': 'football', 'competition': 'ligue1'},
    {'sport': 'football', 'competition': 'liga'},
    {'sport': 'football', 'competition': 'bundesliga'},
    {'sport': 'football', 'competition': 'premier-league'},
    {'sport': 'football', 'competition': 'serie-a'},
    {'sport': 'football', 'competition': 'serie-a-brasil'},
    {'sport': 'football', 'competition': 'a-league'},
    {'sport': 'football', 'competition': 'bundesliga-austria'},
    {'sport': 'football', 'competition': 'division-1a'},
    {'sport': 'football', 'competition': 'super-lig'},
    {'sport': 'basketball', 'competition': 'euroleague'},
    {'sport': 'basketball', 'competition': 'nba'}
]


def main(competition):

    for comp in competition :
        try :
            compet = arb.merge_results(competition=comp)
        except :
            continue

        message = "{}".format(comp)
        # log.discord(message=message) 
        log.log(message)
        if comp['sport'] == 'football' :
            arb.arb_foot(compet)
            print("foot")
        elif comp['sport'] == 'basketball' :
            print("basket")
            arb.arb_basket(compet)

main(competition=competition)
    