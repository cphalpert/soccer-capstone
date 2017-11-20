# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 13:43:19 2017

@author: Feng Ye
"""

import pandas as pd

df_main = pd.read_csv("Main_Data_New.csv")
df_main = df_main.drop("Unnamed: 0", 1)


from datetime import date, datetime

def calculate_age(born):
    born = datetime.strptime(born, "%m/%d/%Y")
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

df_main["age_current"] = df_main["birthday"].apply(calculate_age)

df_whoscored = pd.read_csv("whoscored_v2.csv")

df_combined = df_main.merge(df_whoscored, on=["name", "season", "age_current"])

df_combined.to_csv("Players_Combined_v2.csv", index=False)