# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 13:31:24 2017

@author: Feng Ye
"""

import pandas as pd

df_ws = pd.read_csv("whoscored_data - All_Seasons.csv")

columns_dup = ['Unnamed: 2','R.1','Unnamed: 16','Player.1','Apps.1','Mins.1', \
'Rating.1','R.2','Unnamed: 30','Player.2','Apps.2','Mins.2','Goals.1', \
'Assists.1','SpG.1','Rating.2','R.3','Unnamed: 45','Player.3','Apps.3', \
'Mins.3','Assists.2','KeyP.1','PS%.1','Rating.3']

df_ws.drop(columns_dup, inplace=True, axis=1)
df_ws.rename(columns={'R': 'rank_in_season', 'SpG': 'shots_per_game', \
'PS%': 'pass_success', 'Offsides': 'offside_won', 'Drb': 'drb_past', \
'Drb.1': 'drb', 'Off': 'offside', 'Disp': 'dispossessed', 'UnsTch': 'bad_control', \
'AvgP': 'passes_per_game', 'LongB': 'long_ball', 'ThrB': 'through_ball'}, inplace=True)

import unicodedata

replace_accents = lambda x: unicodedata.normalize('NFD', x).encode('ascii', 'ignore')
df_ws['Player'] = df_ws['Player'].str.decode("utf-8")

df_ws['age_current'] = 0
df_ws['team'] = ""
df_ws['name'] = ""
df_ws['app_start'] = 0
df_ws['app_sub'] = 0

for index, row in df_ws.iterrows():
    player = row['Player'].split(',')
    df_ws.set_value(index, 'age_current', player[1])
    name_team = replace_accents(player[0])
    
    for i in xrange(len(name_team)-1):
        if (name_team[i].islower() and name_team[i+1].isupper()):
            df_ws.set_value(index, 'name', name_team[:i+1])
            df_ws.set_value(index, 'team', name_team[i+1:])
            break
    
    app = row['Apps']
    if app.isdigit():
        df_ws.set_value(index, 'app_start', app)
    else:
        app_list = app.split('(')
        df_ws.set_value(index, 'app_start', app_list[0])
        df_ws.set_value(index, 'app_sub', app_list[1].replace(")", ""))

df_ws.drop(['Player', 'Apps'], inplace=True, axis=1)

df_ws.to_csv("whoscored_v2.csv", index=False)
