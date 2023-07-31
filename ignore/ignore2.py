# ignore.py

import sqlite3
from datetime import datetime, timedelta

# Connect to the SQLite database
conn = sqlite3.connect('found_opp.db')
cursor = conn.cursor()

# Delete all existing rows from the history_opportunities_basket table
cursor.execute('DELETE FROM history_opportunities_basket')

# Define the opportunities you want to add
# Each opportunity is a tuple of (Match, Team1, Team2, Odd_team1_winning, Odd_team2_winning, Team1_site, Team2_site, Returns, Date)
opportunities = [
    ("Match 1", "Team 1", "Team 2", 1.8, 2.2, "Site 1", "Site 2", 5, "2023-06-26 12:00:00"),
    ("Match 2", "Team 3", "Team 4", 1.9, 2.1, "Site 1", "Site 2", 6, "2023-06-27 13:00:00"),
    ("Match 3", "Team 5", "Team 6", 2.0, 2.0, "Site 1", "Site 2", 10, "2023-06-28 14:00:00"),
    ("Match 4", "Team 7", "Team 8", 1.7, 2.3, "Site 1", "Site 2", 7, "2023-06-29 15:00:00"),
    ("Match 5", "Team 9", "Team 10", 1.6, 2.4, "Site 1", "Site 2", 8, "2023-06-30 16:00:00")
]

# Insert the opportunities into the database
cursor.executemany('''
    INSERT INTO history_opportunities_basket (Match, Team1, Team2, Odd_team1_winning, Odd_team2_winning, Team1_site, Team2_site, Returns, Date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', opportunities)


# Delete all existing rows from the opportunities_basket table
cursor.execute('DELETE FROM opportunities_basket')

# Define the opportunities you want to add to opportunities_basket
opportunities_current = [
    ("Match 6", "Team 11", "Team 12", 1.7, 2.3, "Site 1", "Site 2", 5, "2023-07-01 12:00:00"),
    ("Match 3", "Team 5", "Team 6", 2.0, 2.0, "Site 1", "Site 2", 10, "2023-06-28 14:00:00"),
    ("Match 4", "Team 7", "Team 8", 1.7, 2.3, "Site 1", "Site 2", 7, "2023-06-29 15:00:00"),
    ("Match 5", "Team 9", "Team 10", 1.6, 2.4, "Site 1", "Site 2", 8, "2023-06-30 16:00:00")
]

# Insert the opportunities into the opportunities_basket table
cursor.executemany('''
    INSERT INTO opportunities_basket (Match, Team1, Team2, Odd_team1_winning, Odd_team2_winning, Team1_site, Team2_site, Returns, Date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', opportunities_current)

# Commit the changes and close the connection
conn.commit()
conn.close()
