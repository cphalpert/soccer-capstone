# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

arrival_df = pd.read_pickle("arrivals.p")

departure_df = pd.read_pickle("departures.p")

import unicodedata

def df_transform(df, typ):
    df2 = df
    df2 = df2.replace(" Mill. ", "0000", regex=True)
    df2 = df2.replace(" Th. ", "000", regex=True)
    df2 = df2.replace(",", "", regex=True)
    df2 = df2.replace(unicodedata.lookup('EURO SIGN'), '', regex=True)
    
    # Replace accented unicode characters with their ascii equivalents
    replace_accents = lambda x: unicodedata.normalize('NFD', x).encode('ascii', 'ignore')
    df2['team_name'] = df2['team_name'].apply(replace_accents)
    if (typ=="arrivals"):
        df2['Arrivals'] = df2['Arrivals'].apply(replace_accents)
        df2['Moving from'] = df2['Moving from'].apply(replace_accents)
    elif (typ=="departures"):
        df2['Departures'] = df2['Departures'].apply(replace_accents)
        df2['Moving to'] = df2['Moving to'].apply(replace_accents)
    
    return df2

arrival_df = df_transform(arrival_df, "arrivals")
departure_df = df_transform(departure_df, "departures")

arrival_df.to_csv("arrivals.csv", encoding="utf_8")
departure_df.to_csv("departures.csv", encoding="utf_8")