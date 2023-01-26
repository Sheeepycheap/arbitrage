import pandas as pd
import winnamax
import betclic
import netbet
import pmu
import zebet
from difflib import SequenceMatcher
import numpy as np
import log
import sys



def similar(a,b):
    res = []
    for i in range(len(b)) :
        res.append(SequenceMatcher(None,a,b[i]).ratio())
    return np.argmax(res)


def similar_ratio(a,b) :
    res = []
    for i in range(len(b)) :
        res.append(SequenceMatcher(None,a,b[i]).ratio())
    return max(res)
def merge_results(competition):
    matches = []
    win = winnamax.into_a_pd(competition)
    net= netbet.into_a_pd(competition)
    pm = pmu.into_a_pd(competition)
    zeb = zebet.into_a_pd(competition)
    bet = betclic.into_a_pd(competition)
    long = min([len(win),len(net),len(pm),len(zeb),len(bet)])
    for i in range(long) :
        concordance_netbet = similar(win['key'][i],net['key'])
        ratio_netbet = similar_ratio(win['key'][i],net['key'])

        conc_pmu = similar(win['key'][i],pm['key'])
        ratio_pmu = similar_ratio(win['key'][i],pm['key'])

        conc_zebet = similar(win['key'][i],zeb['key'])
        ratio_zebet = similar_ratio(win['key'][i],zeb['key'])

        conc_betclic = similar(win['key'][i],bet['key'])
        ratio_betclic = similar_ratio(win['key'][i],bet['key'])

        if (ratio_netbet < 0.8 or ratio_pmu<0.8 or ratio_zebet<0.8 or ratio_betclic < 0.8) :
            continue
    
        match = [win[i:i+1],net[concordance_netbet:concordance_netbet+1],pm[conc_pmu:conc_pmu+1],zeb[conc_zebet:conc_zebet+1],bet[conc_betclic:conc_betclic+1]]
        match = pd.concat(match)
        match['site'] = ['winnamax','netbet','pmu','zebet','betclic']
        matches.append(match)
    return matches

#competitionn = {'sport': 'basketball', 'competition': 'euroleague'}
#matches = merge_results(competitionn)

def arbitrage_foot_calcul(a,b,c) :
    return (1-(1/a + 1/b + 1/c))*100

def arbitrage_basket_calcul(a,b) :
    return (1-(1/a + 1/b))*100

def gain_2(n,arb,site_a,a,site_b,b) :
    message = " -> Il faut aller sur le bookmaker {} et parier sur l'issue avec la côte {} (Issue A) et aller sur le bookmaker {} et parier sur l'issue avec la côte {} (Issue B)".format(site_a,a,site_b,b)
    MA = n/((1-arb*0.01)*a)
    MB = n/((1-arb*0.01)*b)
    EA = MA*a-n
    EB = MB*b-n
    gain = " -> Gain garantie de {:.2f}% . Par exemple pour {} euros, il faut parier {} sur l'issue A et {} sur l'issue B :".format((EA/n)*100,n,MA,MB)
    outcome_a = " -> Issue A : tu gagneras {}*{} - {} = {} ".format(MA,a,n,EA)
    outcome_b = " -> Issue B : tu gagneras {}*{} - {} = {} ".format(MB,b,n,EB)
    log.discord(message)
    log.discord(gain)
    log.discord(outcome_a)
    log.discord(outcome_b)
    log.log(message)
    log.log(gain)
    log.log(outcome_a)
    log.log(outcome_b)

def gain_3(n,arb,site_a,a,site_b,b,site_c,c) :
    message = " -> Il faut aller sur le bookmaker {} et parier sur l'issue avec la côte {} (Issue A), aller sur le bookmaker {} et parier sur l'issue avec la côte {} (Issue B) et aller sur le bookmaker {} et parier sur l'issue avec la côte {} (Issue B)".format(site_a,a,site_b,b,site_c,c)
    MA = n/((1-arb*0.01)*a)
    MB = n/((1-arb*0.01)*b)
    MC = n/((1-arb*0.01)*c)
    EA = MA*a-n
    EB = MB*b-n
    EC = MC*c-n
    gain = " -> Gain garantie de {:.2f}% . Par exemple pour {} euros, il faut parier {} sur l'issue A, {} sur l'issue B et {} sur l'issue C  :".format((EA/n)*100,n,MA,MB,MC)
    outcome_a = " -> Issue A : tu gagneras {}*{} - {} = {} ".format(MA,a,n,EA)
    outcome_b = " -> Issue B : tu gagneras {}*{} - {} = {} ".format(MB,b,n,EB)
    outcome_c = " -> Issue C : tu gagneras {}*{} - {} = {} ".format(MC,c,n,EC)
    log.discord(message)
    log.discord(gain)
    log.discord(outcome_a)
    log.discord(outcome_b)
    log.discord(outcome_c)
    log.log(message)
    log.log(gain)
    log.log(outcome_a)
    log.log(outcome_b)
    log.log(outcome_c)


#gain_2(1000,11.11,"zebet",1.35,"netbet",6.75)

def arb_foot(matches) :
    for match in matches :
        key = match['key'].values[0]
        a = match['odd of team 1 winning'].values
        c = match['odd of team 2 winning'].values
        b = match['odds of equality '].values
        site = match['site'].values

        log.log("POUR LE MATCH : {}".format(key))
        #log.discord("POUR LE MATCH : {}".format(key))
        for i in range(len(match)) :
            for j in range(len(match)) :
                for k in range(len(match)) :
                    if i==j and i == k :
                        continue
                    else :
                        arb = arbitrage_foot_calcul(a[i],b[j],c[k])
                        log.log(" @{}/{}/{} - {}/{}/{} - le resultat du calcul est : {}".format(a[i],b[j],c[k],site[i],site[j],site[k],arb))

                        if arb > 0 :
                            message = " -> FOUND !!! Vérifiez si les côtes et le match est bien celui annoncé sur les site. Il se peut que l'algorithme confonde certaine équipe, par exemple LA Clippers et LA Lakers."
                            log.discord(message=message)
                            log.discord(" -> POUR LE MATCH : {}".format(key))
                            message = " @{}/{}/{} - {}/{}/{} - le résultat du calcul est : {}".format(a[i],b[j],c[k],site[i],site[j],site[k],arb)
                            log.discord(message=message)
                            log.discord(str(match.to_numpy()))
                            log.log("FOUND !!!")
                            log.log(message)
                            log.log(str(match.to_numpy()))
                            gain_3(1000,arb,site[i],a[i],site[j],b[j],site[k],c[k])
                            log.discord("--")

#"""""""""""""""""""""""""""""""""""""""""#

def arb_basket(matches) :
    for match in matches :
        key = match['key'].values[0]
        a = match['odd of team 1 winning'].values
        b = match['odd of team 2 winning'].values
        site = match['site'].values

        log.log("POUR LE MATCH : {}".format(key))
        #log.discord("POUR LE MATCH : {}".format(key))

        for i in range(len(match)) :
            for j in range(len(match)) :
                if i==j :
                    continue
                else :
                    arb = arbitrage_basket_calcul(a[i],b[j])
                    log.log(" @{}/{} - {}/{} - le résultat du calcul est : {}".format(a[i],b[j],site[i],site[j],arb))
                    
                    if arb > 0 :
                        message = " -> FOUND !!! Vérifiez si les côtes et le match est bien celui annoncé sur les site. Il se peut que l'algorithme confonde certaine équipe, par exemple LA Clippers et LA Lakers."
                        log.discord(message=message)
                        log.discord(" -> POUR LE MATCH : {}".format(key))
                        message = " @{}/{} - {}/{} - le résultat du calcul est : {}".format(a[i],b[j],site[i],site[j],arb)
                        log.discord(message=message)
                        log.discord(str(match.to_numpy()))
                        log.log("FOUND !!!")
                        log.log(message)
                        log.log(str(match.to_numpy()))
                        gain_2(1000,arb,site[i],a[i],site[j],b[j])
                        log.discord("--")

                        
