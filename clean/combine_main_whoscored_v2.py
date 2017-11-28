# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 16:14:19 2017

@author: Feng Ye
"""

import pandas as pd

df_main = pd.read_pickle("market_values.p")
#df_main = df_main.drop("Unnamed: 0", 1)
df_main = df_main.rename(columns={"Player(s)": "name", "year": "season", \
"Nat1": 'nationality', 'Contract until': 'contract_expir', \
'Market value': 'market_val', 'In the team since': 'member_since'})

import unicodedata
from unidecode import unidecode

#replace_accents = lambda x: unicodedata.normalize('NFD', x).encode('ascii', 'ignore')
replace_accents = lambda x: unidecode(x)
df_main['name'] = df_main['name'].apply(replace_accents)

for index, row in df_main.iterrows():
    try: 
        df_main.set_value(index, 'before', replace_accents(row['before']))
    except:
        continue

#df_main['before'] = df_main['before'].apply(replace_accents)

    
df_main['name'] = df_main['name'].str.strip()
df_main['season'] = df_main['season'].astype(int)

df_main = df_main.replace(unicodedata.lookup('POUND SIGN'), '', regex=True)
df_main['market_val'] = df_main['market_val'].str.replace('k', '000')
df_main['market_val'] = df_main['market_val'].str.replace('.', '')
df_main['market_val'] = df_main['market_val'].str.replace('m', '0000')

df_main['Height'] = df_main['Height'].str.replace(' m', '')
df_main['Height'] = df_main['Height'].str.replace(',', '')


from datetime import date, datetime

def calculate_age(born):
    born = datetime.strptime(born, "%b %d, %Y")
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

s = df_main['born/age'].apply(lambda x: x.split('('))
df_main['birthday'] = s.apply(lambda x: x[0].strip())

df_main = df_main[df_main['birthday']!='-']
df_main = df_main[df_main['birthday']!='']
df_main["age_current"] = df_main["birthday"].apply(calculate_age)

columns_drop = ['#', 'born/age', 'Nat2']
df_main.drop(columns_drop, inplace=True, axis=1)

df_ws = pd.read_csv("whoscored_v3.csv")
#df_whoscored = df_whoscored.rename(columns={"player": "name", "Season": "season"})
df_ws = df_ws[df_ws['pos_type']!='Goalkeeper']
df_ws = df_ws[df_ws['Mins']>90]

df_combined = df_main.merge(df_ws, on=["name", "age_current", "season"])

df_combined = df_combined.merge(df_main, on=['name', 'age_current'], how='left')

df_combined = df_combined[df_combined['season_x']==(df_combined['season_y']+1)]

columns_remove = ['nationality_y', 'Height_y', 'Foot_y', 'member_since_y', \
'before_y', 'contract_expir_y','team_name_y', 'season_y', 'birthday_y']

df_combined.drop(columns_remove, inplace=True, axis=1)

df_combined.rename(columns={'nationality_x': 'nationality', 'Height_x': 'height',
'Foot_x': 'preferred_foot', 'member_since_x': 'member_since', \
'before_x': 'team_before', 'contract_expir_x': 'contract_expir', \
'market_val_x': 'market_val','team_name_x': 'team_name', 'season_x': 'season', \
'birthday_x': 'birthday', 'market_val_y': 'market_val_prev'}, inplace=True)
df_combined = df_combined.drop_duplicates()

df_combined['team_name'] = df_combined['team_name'].str.replace("-", " ")
df_combined['team'] = df_combined['team'].str.lower()

df_combined['is_match'] = ''
for index, row in df_combined.iterrows():
    result = row['team'] in row['team_name']
    df_combined.set_value(index, 'is_match', result)    

df_combined = df_combined[df_combined['is_match']==True]

df_combined['market_val'] = df_combined['market_val'].str.replace('-', '0')
df_combined['market_val_prev'] = df_combined['market_val_prev'].str.replace('-', '0')

df_combined['market_val'] = df_combined['market_val'].astype(int)
df_combined['market_val_prev'] = df_combined['market_val_prev'].astype(int)
df_combined.to_csv("Players_Combined_v3.csv", index=False)