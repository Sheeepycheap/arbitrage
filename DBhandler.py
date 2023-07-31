import sqlite3
import datetime


# Create the table if not already
connection = sqlite3.connect('found_opp.db')
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS opportunities_foot (
    id INT,
    Match TEXT,
    Team1 TEXT,
    Team2 TEXT,
    Odd_team1_winning FLOAT,
    Odd_equality_b FLOAT,
    Odd_team2_winning FLOAT,
    Team1_site TEXT,
    Equality_site TEXT,
    Team2_site TEXT,
    Returns FLOAT,
    Date TEXT
    )
""") 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS history_opportunities_foot (
    id INT,
    Match TEXT,
    Team1 TEXT,
    Team2 TEXT,
    Odd_team1_winning FLOAT,
    Odd_equality_b FLOAT,
    Odd_team2_winning FLOAT,
    Team1_site TEXT,
    Equality_site TEXT,
    Team2_site TEXT,
    Returns FLOAT,
    Date TEXT
    )
""") 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS history_opportunities_basket (
    id INT,
    Match TEXT,
    Team1 TEXT,
    Team2 TEXT,
    Odd_team1_winning FLOAT,
    Odd_equality_b FLOAT,
    Odd_team2_winning FLOAT,
    Team1_site TEXT,
    Equality_site TEXT,
    Team2_site TEXT,
    Returns FLOAT,
    Date TEXT
    )
""") 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS opportunities_basket (
    id INT,
    Match TEXT,
    Team1 TEXT,
    Team2 TEXT,
    Odd_team1_winning FLOAT,
    Odd_team2_winning FLOAT,
    Team1_site TEXT,
    Team2_site TEXT,
    Returns FLOAT,
    Date TEXT
    )
""") 
connection.commit()
connection.close()


class Opp_football():
    def __init__(self,key,team1,team2,odd_team1_w,odd_team2_w,odd_equality,site_team1,site_equ,site_team2,arb) -> None:
        self.connection = sqlite3.connect('found_opp.db')
        self.cursor = self.connection.cursor()

        self.key = key
        self.team1 = team1
        self.team2 = team2
        self.odd_team1_w = odd_team1_w
        self.odd_team2_w = odd_team2_w
        self.odd_equ = odd_equality
        self.site_team1 = site_team1
        self.site_equ = site_equ
        self.site_team2 = site_team2
        self.arb = arb

    def close(self) -> None:
        self.connection.commit()
        self.connection.close()
    
    def add(self) -> None:
        query = "SELECT COUNT(*) FROM opportunities_foot"
        self.cursor.execute(query)
        id = self.cursor.fetchone()[0]
        now = datetime.datetime.now().replace(microsecond=0)

        query = "INSERT INTO opportunities_foot (id, Match, Team1, Team2, Odd_team1_winning, Odd_equality_b, Odd_team2_winning, Team1_site, Equality_site, Team2_site, Returns, Date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        data = (id,self.key ,self.team1 ,self.team2 ,self.odd_team1_w ,self.odd_equ ,self.odd_team2_w ,self.site_team1 ,self.site_equ ,self.site_team2,self.arb,now)
        self.cursor.execute(query, data)
        self.connection.commit()
    
    def histo_add(self) -> None:
        query = "SELECT COUNT(*) FROM history_opportunities_foot"
        self.cursor.execute(query)
        id = self.cursor.fetchone()[0]
        now = datetime.datetime.now().replace(microsecond=0)

        query = "INSERT INTO history_opportunities_foot (id, Match, Team1, Team2, Odd_team1_winning, Odd_equality_b, Odd_team2_winning, Team1_site, Equality_site, Team2_site, Returns, Date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        data = (id,self.key ,self.team1 ,self.team2 ,self.odd_team1_w ,self.odd_equ ,self.odd_team2_w ,self.site_team1 ,self.site_equ ,self.site_team2,self.arb,now)
        self.cursor.execute(query, data)
        self.connection.commit()
        
    def getId(self) -> int :
        self.cursor.execute("SELECT id FROM opportunities_foot WHERE Match=? AND Team1_site=? AND Equality_site=? AND Team2_site=?", (self.key, self.site_team1, self.site_equ, self.site_team2))
        result = self.cursor.fetchone()

        if result is not None :
            result = result[0]
            return result
        else :
            return None

    def print_if_exist(self) -> None :
        id = self.getId()
        if id is not None :
            query = "SELECT * FROM opportunities_foot WHERE id = {}".format(id)
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row is not None :
                print(row)
        else : 
            print("Row not found")
            
    def delete(self) -> None:
        #id = self.getId() 
        query = "DELETE FROM opportunities_foot WHERE Match=? AND Team1_site=? AND Equality_site=? AND Team2_site=?"
        self.cursor.execute(query, (self.key, self.site_team1, self.site_equ, self.site_team2))
        self.connection.commit()


    def check_existance(self) -> bool :
        id = self.getId()
        if id is not None :
            return True
        else :
            return False
    
    def remove_duplicates(self) -> None:
        self.cursor.execute("""
            CREATE TEMPORARY TABLE temp_table AS
            SELECT *
            FROM (
                SELECT *,
                    ROW_NUMBER() OVER (PARTITION BY Match, Team1_site, Equality_site, Team2_site, date(substr(Date, 1, 10)) ORDER BY Returns DESC, Date DESC) AS row_num
                FROM history_opportunities_foot
            )
            WHERE row_num = 1;
        """)
        self.cursor.execute("DROP TABLE history_opportunities_foot;")
        self.cursor.execute("""
            CREATE TABLE history_opportunities_foot AS
            SELECT id, Match, Team1, Team2, Odd_team1_winning, Odd_equality_b, Odd_team2_winning, Team1_site, Equality_site, Team2_site, Returns, Date
            FROM temp_table;
        """)
        self.cursor.execute("DROP TABLE temp_table;")
        self.connection.commit()

        

class Opp_basket():
    def __init__(self, key, team1, team2, odd_team1_w, odd_team2_w, site_team1, site_team2, arb) -> None:
        self.connection = sqlite3.connect('found_opp.db')
        self.cursor = self.connection.cursor()

        self.key = key
        self.team1 = team1
        self.team2 = team2
        self.odd_team1_w = odd_team1_w
        self.odd_team2_w = odd_team2_w
        self.site_team1 = site_team1
        self.site_team2 = site_team2
        self.arb = arb

    def close(self) -> None:
        self.connection.commit()
        self.connection.close()

    def add(self) -> None:
        query = "SELECT COUNT(*) FROM opportunities_basket"
        self.cursor.execute(query)
        id = self.cursor.fetchone()[0]
        now = datetime.datetime.now().replace(microsecond=0)

        query = "INSERT INTO opportunities_basket (id, Match, Team1, Team2, Odd_team1_winning, Odd_team2_winning, Team1_site, Team2_site, Returns, Date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        data = (id, self.key, self.team1, self.team2, self.odd_team1_w, self.odd_team2_w, self.site_team1, self.site_team2, self.arb, now)
        self.cursor.execute(query, data)
        self.connection.commit()

    def histo_add(self) -> None:
        query = "SELECT COUNT(*) FROM history_opportunities_basket"
        self.cursor.execute(query)
        id = self.cursor.fetchone()[0]
        now = datetime.datetime.now().replace(microsecond=0)

        query = "INSERT INTO history_opportunities_basket (id, Match, Team1, Team2, Odd_team1_winning, Odd_team2_winning, Team1_site, Team2_site, Returns, Date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        data = (id, self.key, self.team1, self.team2, self.odd_team1_w, self.odd_team2_w, self.site_team1, self.site_team2, self.arb, now)
        self.cursor.execute(query, data)
        self.connection.commit()

    def getId(self) -> int :
        self.cursor.execute("SELECT id FROM opportunities_basket WHERE Match=? AND Team1_site=? AND Team2_site=?", (self.key, self.site_team1, self.site_team2))
        result = self.cursor.fetchone()

        if result is not None :
            result = result[0]
            return result
        else :
            return None

    def print_if_exist(self) -> None :
        id = self.getId()
        if id is not None :
            query = "SELECT * FROM opportunities_basket WHERE id = {}".format(id)
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row is not None :
                print(row)
        else : 
            print("Row not found")

    def delete(self) -> None :
        id = self.getId() 
        query = "DELETE FROM opportunities_basket WHERE id = {}".format(id)
        self.cursor.execute(query)
        self.connection.commit()

    def check_existance(self) -> bool :
        id = self.getId()
        if id is not None :
            return True
        else :
            return False
        
    def remove_duplicates(self) -> None :
        self.cursor.execute("""
            CREATE TEMPORARY TABLE temp_table AS
            SELECT *
            FROM (
                SELECT *,
                    ROW_NUMBER() OVER (PARTITION BY Match, Team1_site, Team2_site, date(substr(Date, 1, 10)) ORDER BY Returns DESC, Date DESC) AS row_num
                FROM history_opportunities_basket
            )
            WHERE row_num = 1;
        """)
        self.cursor.execute("DROP TABLE history_opportunities_basket;")
        self.cursor.execute("""
            CREATE TABLE history_opportunities_basket AS
            SELECT id, Match, Team1, Team2, Odd_team1_winning, Odd_team2_winning, Team1_site, Team2_site, Returns, Date
            FROM temp_table;
        """)
        self.cursor.execute("DROP TABLE temp_table;")
        self.connection.commit()

        

conn = sqlite3.connect('found_opp.db')
cursor = conn.cursor()


def delete_all_hist(cursor,connection) -> None:
    query = "DELETE FROM history_opportunities_foot"
    cursor.execute(query)
    connection.commit()

    query = "DELETE FROM history_opportunities_basket"
    cursor.execute(query)
    connection.commit()

def delete_all(cursor,connection) -> None:
    query = "DELETE FROM opportunities_foot"
    cursor.execute(query)
    connection.commit()

    query = "DELETE FROM opportunities_basket"
    cursor.execute(query)
    connection.commit()



delete_all(cursor,conn)
#delete_all_hist(cursor,conn)

# Close the database connection
conn.close()
















# test = Opp_football('PSGvBayern','PSG','Bayern',1.5,1.5,1.5,'Netclic','winnamax','winnamax',10.0)
# test.histo_add()
# test.print_if_exist()
# test.close()




# sql = "INSERT INTO opportunities_foot (id, Match, Team1, Team2, Odd_team1_winning, Odd_equality_b, Odd_team2_winning, Team1_site, Equality_site, Team2_site, Date) VALUES (1, 'Match A', 'Team 1', 'Team 2', 2.5, 3.0, 4.0, 'Site 1', 'Site 2', 'Site 3', datetime('now', 'localtime'))"
# rows = cursor.fetchall()
# print(rows)