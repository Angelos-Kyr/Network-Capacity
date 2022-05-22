import configparser
import sqlite3

from helper import enum


class Database:
    DB_LOCATION = 'net_stats.db'

    COLUMNS = enum(id=0, net=1, net_usage=2, dhcp_usage=3, timestamp=4)

    def __init__(self, db_location=None):

        config = configparser.ConfigParser()
        config.read('config.ini')
        DB_LOCATION = config['local']['database']

        if db_location is not None:
            self.connection = sqlite3.connect(db_location)
        else:
            self.connection = sqlite3.connect(self.DB_LOCATION)
        self.cur = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def execute(self, new_data):
        self.cur.execute(new_data)

    def query(self, statement):
        self.cur.execute(statement)
        rows = self.cur.fetchall()
        return rows

    def get_all(self):
        self.cur.execute("SELECT * FROM net_stats")
        rows = self.cur.fetchall()
        return rows

    def get_by_netname(self, networkname):
        sqlite_select_query = """SELECT * from net_stats where net = ?"""
        self.cur.execute(sqlite_select_query, (networkname,))
        return self.cur.fetchall()

    # data: (date: timestamp, net:str, net_usage:float, dhcp_usage:float)
    def add(self, data):
        self.create_table()
        self.cur.execute('INSERT INTO net_stats VALUES(NULL, ?, ?, ?, ?)', data)
        self.commit()

    def create_table(self):
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS net_stats(
         ID INTEGER PRIMARY KEY,
         TIMESTAMP DATE,
         NET TEXT,
         NET_USAGE FLOAT, 
         DHCP_USAGE FLOAT)
         ''')

    def commit(self):
        self.connection.commit()
