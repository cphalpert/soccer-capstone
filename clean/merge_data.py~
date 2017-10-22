"""
Merge the cleaned transfermarket data with the kaggle data set

Merge based on player name. Need to resolve any duplicates / fuzzy matches that occur.
"""

import sqlite3
import pandas as pd

SQL_FILE = '../data/database.sqlite'

TRANSFERMARKET_FILE = '../data/clean_transfermarket.p'

show_tables_query = """SELECT name FROM sqlite_master
WHERE type='table'
ORDER BY name;"""

conn = sqlite3.connect(SQL_FILE)

all_tables = pd.read_sql_query(show_tables_query, conn)


all_players = pd.read_sql_query("""select player_name from Player""", conn)

# TODO: Need to figure out which duplicate player name to preserve
distinct_players = pd.DataFrame(all_players['player_name'].unique(), columns=['player_name'])



tmkt = pd.read_pickle(TRANSFERMARKET_FILE)

joined_players = tmkt.merge(distinct_players, left_on='Name', right_on='player_name', how='inner')
