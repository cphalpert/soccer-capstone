# -*- coding: utf-8 -*-
"""
Spyder Editor

Author: Feng Ye
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

#arrival_df.to_csv("arrivals.csv", encoding="utf_8")
#departure_df.to_csv("departures.csv", encoding="utf_8")

arrival_df.columns = ['index', 'name', 'age', 'nationality', 'position', 'pos', 'market_val', 'club_from', \
                      'country_from', 'transfer_fee', 'club_to', 'season']
arrival_df["country_to"] = "Spain"

departure_df.columns = ['index', 'name', 'age', 'nationality', 'position', 'pos', 'market_val', 'club_to', \
                        'country_to', 'transfer_fee', 'club_from', 'season']
departure_df['country_from'] = "Spain"

main_df = arrival_df.append(departure_df, ignore_index=True)

main_df = main_df.drop("index", 1)
main_df = main_df.drop_duplicates()
#main_df[main_df['name']=='Florent Sinama-Pongolle']
main_df.to_csv("Combined_Transfers.csv")