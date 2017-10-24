# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 15:39:20 2017

@author: ralph8611
"""

import sqlite3
conn = sqlite3.connect("database.sqlite")
c = conn.cursor()

#table1 = 'Player_Attributes'
#table2 = 'Player'

sql = "select t2.player_name, date(t2.birthday), t2.height, t2.weight, m3.* from ( \
select m2.player_api_id, m2.season, avg(m2.overall_rating), avg(potential), max(preferred_foot) \
,avg(crossing), avg(finishing), avg(heading_accuracy) \
,avg(short_passing), avg(volleys), avg(dribbling) \
,avg(curve), avg(free_kick_accuracy), avg(long_passing) \
,avg(ball_control), avg(acceleration) \
,avg(sprint_speed), avg(agility), avg(reactions), avg(balance) \
,avg(shot_power), avg(jumping), avg(stamina) \
,avg(strength), avg(long_shots), avg(aggression), avg(interceptions) \
,avg(positioning), avg(vision) \
,avg(penalties), avg(marking), avg(standing_tackle) \
,avg(sliding_tackle), avg(gk_diving), avg(gk_handling) \
,avg(gk_kicking), avg(gk_positioning), avg(gk_reflexes) \
from ( \
select (case when strftime('%m', m.date)>='08' \
then cast(strftime('%Y', m.date) as INT) \
else strftime('%Y', m.date)-1 end) as season, m.* \
from Player_Attributes m) m2 \
group by m2.player_api_id, m2.season) m3 \
join Player t2 on m3.player_api_id=t2.player_api_id"

c.execute(sql)

#c.fetchall()

import pandas as pd
player_df = pd.read_sql(sql, conn)
player_df.columns = ['name', 'birthday', 'height', 'weight', 'player_api_id', 'season', 'overall_rating', 'potential', \
                     'preferred_foot', 'crossing', 'finishing', 'heading_accuracy', 'short_passing', 'volleys', 'dribbling', \
                    'curve', 'free_kick_accuracy', 'long_passing', 'ball_control', 'acceleration', 'sprint_speed', 'agility', \
                    'reactions', 'balance', 'shot_power', 'jumping', 'stamina', 'strength', 'long_shots', 'aggression', \
                    'interceptions', 'positioning', 'vision', 'penalties', 'marking', 'standing_tackle', 'sliding_tackle', \
                    'gk_diving', 'gk_handling', 'gk_kicking', 'gk_positioning', 'gk_reflexes']
player_df.to_csv("Player_Metrics.csv")