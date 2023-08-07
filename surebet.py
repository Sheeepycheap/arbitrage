from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/surebet.html')
def surebet():
    conn = sqlite3.connect('found_opp.db')
    cursor = conn.cursor()

    # Récupère les opportunités de football
    cursor.execute('SELECT Match, Team1, Team2, Odd_team1_winning, Odd_equality_b, Odd_team2_winning, Team1_site, Equality_site, Team2_site, Returns, Date FROM opportunities_foot')
    rows_foot = cursor.fetchall()

    # Récupère les opportunités de basket
    cursor.execute('SELECT Match, Team1, Team2, Odd_team1_winning, Odd_team2_winning, Team1_site, Team2_site, Returns, Date FROM opportunities_basket')
    rows_basket = cursor.fetchall()

    return render_template('surebet.html', rows_foot=rows_foot, rows_basket=rows_basket)


@app.route('/historique.html')
def history():
    conn = sqlite3.connect('found_opp.db')
    cursor = conn.cursor()

    # Récupère et trie les opportunités de football par date
    cursor.execute('SELECT Match, Team1, Team2, Odd_team1_winning, Odd_equality_b, Odd_team2_winning, Team1_site, Equality_site, Team2_site, Returns, Date FROM history_opportunities_foot')
    rows_foot = cursor.fetchall()

    # Récupère et trie les opportunités de basket par date
    cursor.execute('SELECT Match, Team1, Team2, Odd_team1_winning, Odd_team2_winning, Team1_site, Team2_site, Returns, Date FROM history_opportunities_basket')
    rows_basket = cursor.fetchall()

    # Fusionner et trier les opportunités
    all_rows = rows_foot + [(r[0], r[1], r[2], r[3], "N/A", r[4], r[5], "N/A", r[6], r[7], r[8]) for r in rows_basket]

    if all_rows:
        all_rows.sort(key=lambda row: row[10])  # Trier par date

        # Calculer le gain total
        total_returns = 1
        portfolio_values = [1000]  # Valeur initiale du portefeuille
        dates = [all_rows[0][10]]  # Date de la première opportunité
        for row in all_rows:
            total_returns *= 1 + row[9]/100  # Converti le pourcentage en format décimal
            new_value = portfolio_values[-1] * (1 + row[9] / 100)
            portfolio_values.append(new_value)
            dates.append(row[10])

        total_returns_percent = (total_returns - 1) * 100  # Converti le résultat final en pourcentage
    else:
        # Set defaults if there are no rows
        total_returns_percent = 0
        dates = []
        portfolio_values = []

    return render_template('historique.html', rows_foot=rows_foot, rows_basket=rows_basket, total_returns=total_returns_percent, dates=dates, portfolio_values=portfolio_values)



if __name__ == '__main__':
    app.run(debug=True,port=8000)
