import sqlite3
import datetime

conn = sqlite3.connect('found_opp.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM opportunities_foot")
print("\n ")
print("opportunities_foot table :")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("SELECT * FROM history_opportunities_foot")
print("\n ")
print("history_opportunities_foot table :")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("SELECT * FROM opportunities_basket")
print("\n ")
print("opportunities_basket table :")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("SELECT * FROM history_opportunities_basket")
print("\n ")
print("history_opportunities_foot basket :")
rows = cursor.fetchall()
for row in rows:
    print(row)

print("\n ")
print("----------------------------------")

def remove_duplicates(cursor, connection):
    # Création d'une table temporaire pour stocker les données uniques
    cursor.execute("""
        CREATE TEMPORARY TABLE temp_table AS
        SELECT *
        FROM (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY Match, Team1_site, Equality_site, Team2_site, date(substr(Date, 1, 10)) ORDER BY Returns DESC, Date DESC) AS row_num
            FROM history_opportunities_foot
        )
        WHERE row_num = 1;
    """)

    # Suppression de la table d'origine
    cursor.execute("DROP TABLE history_opportunities_foot;")

    # Recréation de la table d'origine avec les données uniques de la table temporaire
    cursor.execute("""
        CREATE TABLE history_opportunities_foot AS
        SELECT id, Match, Team1, Team2, Odd_team1_winning, Odd_equality_b, Odd_team2_winning, Team1_site, Equality_site, Team2_site, Returns, Date
        FROM temp_table;
    """)

    # Suppression de la table temporaire
    cursor.execute("DROP TABLE temp_table;")

    # Validation des changements
    connection.commit()


remove_duplicates(cursor,conn)
# Close the database connection


cursor.execute("SELECT * FROM opportunities_foot")
print("\n ")
print("opportunities_foot table :")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("SELECT * FROM history_opportunities_foot")
print("\n ")
print("history_opportunities_foot table :")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("SELECT * FROM opportunities_basket")
print("\n ")
print("opportunities_basket table :")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("SELECT * FROM history_opportunities_basket")
print("\n ")
print("history_opportunities_foot basket :")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()