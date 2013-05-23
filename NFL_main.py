import parse_gameid as pg
import csv
import pandas as pd
import re
import sys

data = pd.read_csv("2002_nfl_pbp_data.csv")

#For PlayType function
data['play_type'] = 'run'
for i in data.index:	
	if('pass' in data['description'][i]) or ('sacked' in data['description'][i]):
		data['play_type'][i] = 'pass'
	if('punts' in data['description'][i]):
		data['play_type'][i] = 'punt'
	if('kicks' in data['description'][i]) and (data['play_type'][i] != 'pass') and (data['play_type'][i] != 'punt'):
		data['play_type'][i] = 'kick'
	
# each entry in gamedata will be a tuple, arranged date, matchup, away, home
gameid = list(data['gameid'])
gamedata = [pg.parse_gameid(i) for i in gameid]

#yards  WHY CAN'T I REFERENCE 'i+1' IN THE LOOP ? AND IS 'hometeam' ONLY USABLE WITHIN 'parse_gameid' ?
yardline = data['ydline']

for i in hometeam:
	if hometeam[i] == hometeam[i+1]:
		i.yards_gained = (yardline[i+1] - yardline[i])
	else:
		i.yards_gained = None