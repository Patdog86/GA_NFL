
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

for i in range(len(data)):
	data['description'][i] = ' '.join(data['description'][i].split())

#For PlayType function
playtype = ['run']*len(data)	
for i in data.index:	
	if ('field goal' in data['description'][i]) or ('Field Goal' in data['description'][i]):
		playtype[i] = 'field goal'
	if('pass' in data['description'][i]) or ('sacked' in data['description'][i]):
		playtype[i] = 'pass'
	if('punts' in data['description'][i]):
		playtype[i] = 'punt'
	if('kicks' in data['description'][i]) and (playtype[i] != 'pass') and (playtype[i] != 'punt'):
		playtype[i] = 'kickoff'
 

# TURNOVERS #
interception = [0]*len(data)
fumble = [0]*len(data)

for i in range(len(data)-1):
	if ('FUMBLE' in data['description'][i]) and (offense[i] != offense[i+1]) and (playtype[i] != 'kickoff'):
		fumble[i] = 1
	elif ('FUMBLE' in data['description'][i]) and (offense[i] == offense[i+1]) and (playtype[i] == 'kickoff'):
		fumble[i] = 1
	elif ('INTERCEPTED' in data['description'][i]) and (offense[i] != offense[i+1]):
		interception[i] = 1
		
home_turnovers = [0]*len(data)
away_turnovers = [0]*len(data)

for i in range(len(data)-1):
	if (hometeam[i] == offense[i]) and (gameid[i] == gameid[i-1]) and ((interception[i] == 1) or (fumble[i] == 1)):
		home_turnovers[i] = (home_turnovers[i-1] + 1)
	elif (playtype[i] == 'kickoff') and (offense[i] == offense[i+1] == awayteam[i]) and (fumble[i] == 1):
		home_turnovers[i] = (home_turnovers[i-1] + 1) 
	elif gameid[i] == gameid[i-1]:
		home_turnovers[i] = home_turnovers[i-1]
for i in range(len(data)-1):		
	if (awayteam[i] == offense[i]) and (gameid[i] == gameid[i-1]) and ((interception[i] == 1) or (fumble[i] == 1)):
		away_turnovers[i] = (away_turnovers[i-1] + 1)
	elif (playtype[i] == 'kickoff') and (offense[i] == offense[i+1] == hometeam[i]) and (fumble[i] == 1):
		away_turnovers[i] = (away_turnovers[i-1] + 1) 
	elif gameid[i] == gameid[i-1]:
		away_turnovers[i] = away_turnovers[i-1]
		
#Parsing gameid variable
gameid = list(data['gameid'])	
date = [i.split('_',1)[0] for i in gameid]
matchup = [i.split('_',1)[1] for i in gameid]
awayteam = [i.split('@',1)[0] for i in matchup]
hometeam = [i.split('@',1)[1] for i in matchup]
	
#gamedata = [pg.parse_gameid(i) for i in gameid]

# YARDS GAINED #
yardline = list(data['ydline'])
offense = list(data['off'])
defense = list(data['def'])

yards_gained_play = [0]*len(yardline)
home_yards_gained_game = [0]*len(yardline)
away_yards_gained_game = [0]*len(yardline)

for i in range(len(hometeam)-1):
	if offense[i] == offense[i+1]:	
		yards_gained_play[i] = (yardline[i] - yardline[i+1])

for i in range(len(data)-1):
	if (offense[i] == hometeam[i]) and (gameid[i] == gameid[i-1]):
		home_yards_gained_game[i] = (home_yards_gained_game[i-1] + yards_gained_play[i])
		away_yards_gained_game[i] = away_yards_gained_game[i-1]
	elif (offense[i] == awayteam[i]) and (gameid[i] == gameid[i-1]):
		away_yards_gained_game[i] = (away_yards_gained_game[i-1] + yards_gained_play[i])
		home_yards_gained_game[i] = home_yards_gained_game[i-1]

# PENALTIES # 
penalty = [0]*len(data)
penalty_enforced = [0]*len(data)
penalty_yards = [0]*len(data)
for i in range(len(data)-1):
	if ('PENALTY' in data['description'][i]):
		penalty[i] = 1
		penalty_enforced[i] = 1
	elif ('Penalty' in data['description'][i]):
		penalty[i] = 1
before_penalty = [None]*len(data)
keyword = ['yards enforced']*len(data)
after_penalty = [None]*len(data)
for i in range(len(data)):
	mystring = data['description'][i]	
	before_penalty[i], keyword[i], after_penalty[i] = mystring.partition(keyword[i])
	before_penalty[i] = ' '.join(before_penalty[i].split())

for i in range(len(data)):
	if keyword[i] != '':
		penalty_yards[i] = int(before_penalty[i].split()[-1])

# CREATING OFFENSE AND DEFENSE SCORE VARIABLES #
homescore = [0]*len(data)
awayscore = [0]*len(data)
offscore = data['offscore']
defscore = data['defscore']

#finds score of home team
for i in range(len(homescore)):
	if hometeam[i] == offense[i]:
		homescore[i] = offscore[i]
	elif hometeam[i] == defense[i]:
		homescore[i] = defscore[i]
		
#finds score of away team
for i in range(len(awayscore)):
	if awayteam[i] == offense[i]:
		awayscore[i] = offscore[i]
	elif awayteam[i] == defense[i]:
		awayscore[i] = defscore[i]
		
# TOTAL SCORE
total_score = [awayscore[i]+homescore[i] for i in range(len(data)-1)]
home_ppg = [0]*len(data)
away_ppg = [0]*len(data)

# IDENTIFYING LAST PLAY OF GAME
final_plays = []
for i in range(len(data)-1):
	if gameid[i] != gameid[i+1]:
		final_plays.append(data.ix[i])
final_plays.append(data.ix[len(data)-1])

"""
# CREATING FINAL FINAL PLAY VARIABLE #
final_play = [0]*len(data)
final_play[len(data)-1] = 1
for i in range(len(data)):
	if gameid[i] != gameid[i-1]:
		final_play[i] = 1
teams = list(set(hometeam))
"""

#identifying winner
homewins = [0]*len(data)
for i in range(len(final_plays)-1):
	if homescore > awayscore:
		homewins = 1
	if homescore == awayscore:
		homewins = 0.5
#home team margin of victory
homediff = [0]*len(data)
for i in range(len(final_plays)-1):
	homediff[i] = (homescore[i] - awayscore[i])
	
#Calculate seconds per play
Seconds_Left = (data['min']*60 + data['sec'])
Seconds_Taken = Seconds_Left
for i in range(len(Seconds_Taken)-1):
	if gameid[i] == gameid[i+1]:
		Seconds_Taken[i] = (Seconds_Left[i] - Seconds_Left[i+1])

#Calculate running time of possession		
Home_TOP = [0]*len(data)
Away_TOP = [0]*len(data)
for i in range(len(Seconds_Taken)-1):
	if (offense[i] == hometeam[i]) and (gameid[i] == gameid[i-1]):
		Home_TOP[i] = (Home_TOP[i-1] + Seconds_Taken[i])
		Away_TOP[i] = Away_TOP[i-1]
	elif (offense[i] == awayteam[i]) and (gameid[i] == gameid[i-1]):
		Away_TOP[i] = (Away_TOP[i-1] + Seconds_Taken[i])
		Home_TOP[i] = Home_TOP[i-1]
		
#Play type per game
home_run = [0]*len(data)
home_pass = [0]*len(data)
home_kick = [0]*len(data)
home_punt = [0]*len(data)
away_run = [0]*len(data)
away_pass = [0]*len(data)
away_kick = [0]*len(data)
away_punt = [0]*len(data)

for i in range(len(data)):
	if (playtype[i] == 'run') and (hometeam[i] == offense[i]) and (gameid[i] == gameid[i-1]):
		home_run[i] = (home_run[i-1]+1)
	elif gameid[i] != gameid[i-1]:
		home_run[i] == 0
	else:
		home_run[i] = home_run[i-1]
for i in range(len(data)):
	if (playtype[i] == 'pass') and (hometeam[i] == offense[i]) and (gameid[i] == gameid[i-1]):
		home_pass[i] = (home_pass[i-1]+1)
	elif gameid[i] != gameid[i-1]:
		home_pass[i] == 0
	else:
		home_pass[i] = home_pass[i-1]
for i in range(len(data)):
	if (playtype[i] == 'kick') and (hometeam[i] == offense[i]) and (gameid[i] == gameid[i-1]):
		home_kick[i] = (home_kick[i-1]+1)
	elif gameid[i] != gameid[i-1]:
		home_kick[i] == 0
	else:
		home_kick[i] = home_kick[i-1]
for i in range(len(data)):
	if (playtype[i] == 'punt') and (hometeam[i] == offense[i]) and (gameid[i] == gameid[i-1]):
		home_punt[i] = (home_punt[i-1]+1)
	elif gameid[i] != gameid[i-1]:
		home_punt[i] == 0
	else:
		home_punt[i] = home_punt[i-1]
for i in range(len(data)):
	if (playtype[i] == 'run') and (awayteam[i] == offense[i]) and (gameid[i] == gameid[i-1]):
		away_run[i] = (away_run[i-1]+1)
	elif gameid[i] != gameid[i-1]:
		away_run[i] == 0
	else:
		away_run[i] = away_run[i-1]
for i in range(len(data)):
	if (playtype[i] == 'pass') and (awayteam[i] == offense[i]) and (gameid[i] == gameid[i-1]):
		away_pass[i] = (away_pass[i-1]+1)
	elif gameid[i] != gameid[i-1]:
		away_pass[i] == 0
	else:
		away_pass[i] = away_pass[i-1]
for i in range(len(data)):
	if (playtype[i] == 'kick') and (awayteam[i] == offense[i]) and (gameid[i] == gameid[i-1]):
		away_kick[i] = (away_kick[i-1]+1)
	elif gameid[i] != gameid[i-1]:
		away_kick[i] == 0
	else:
		away_kick[i] = away_kick[i-1]
for i in range(len(data)):
	if (playtype[i] == 'punt') and (awayteam[i] == offense[i]) and (gameid[i] == gameid[i-1]):
		away_punt[i] = (away_punt[i-1]+1)
	elif gameid[i] != gameid[i-1]:
		away_punt[i] == 0
	else:
		away_punt[i] = away_punt[i-1]


###  grouped_data_game = data.groupby('gameid')  ###
###  grouped_data.tail(1)['offscore'] = offense's score at the end of each game  ###
###  grouped_data['ydline'].max() = the longest yards to go for either team in a given game  ###			