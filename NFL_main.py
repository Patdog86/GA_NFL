import csv
import pdb
import re
import sys

import pandas as pd
#<<<<<<< HEAD
import re
import sys
#=======
#import play_parser
from pandas import *    # 1 pandas is already here 2 * imports are confusing

import parse_gameid as pg
#>>>>>>> e7e7159973ed741276864e8ccc4338ac0067985b

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
"""
gameid = list(data['gameid'])
date = None	
date = [i.split('_',1)[0] for i in gameid]
matchup = None
matchup = [i.split('_',1)[1] for i in gameid]
awayteam = None
awayteam = [i.split('@',1)[0] for i in gameid]
hometeam = None
hometeam = [i.split('@',1)[1] for i in gameid]
"""
gamedata = [pg.parse_gameid(i) for i in gameid]

#yards  WHY CAN'T I REFERENCE 'i+1' IN THE LOOP ? AND IS 'hometeam' ONLY USABLE WITHIN 'parse_gameid' ?
yardline = list(data['ydline'])
yards_gained = [None]*len(yardline)		
for i in [0,len(hometeam)-2]:
	if i < (len(hometeam)-1) and hometeam[i] == hometeam[i+1]:	
		yards_gained[i] = (yardline[i+1] - yardline[i])
