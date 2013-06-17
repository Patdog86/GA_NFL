#<<<<<<< HEAD
import csv
import pdb
import re
import sys
import statsmodels
import numpy as np
import pandas as pd
import re
import math
import matplotlib
import pylab as pl
#=======
#import play_parser

#import parse_gameid as pg
np.random.seed(0)

data = pd.read_csv("/Users/patrickmcnamara/Documents/GA_DataScience/PBPData/Data/NFL_PBP_DATA_2002to2012.csv")

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
		playtype[i] = 'kick'
	
#Parsing gameid variable
gameid = list(data['gameid'])	
date = [i.split('_',1)[0] for i in gameid]
matchup = [i.split('_',1)[1] for i in gameid]
awayteam = [i.split('@',1)[0] for i in matchup]
hometeam = [i.split('@',1)[1] for i in matchup]
home_timezone = [0]*len(data)
away_timezone = [0]*len(data)
season = data['season']
playoffs = data['Playoffs']
for i in range(len(data)):
	if hometeam[i] in ('MIA', 'CAR', 'ATL', 'NYJ', 'BAL', 'NYG', 'NE', 'TB', 'PIT', 'WAS', 'JAC', 'PHI', 'BUF'):
		home_timezone[i] = 3
	if hometeam[i] in ('MIN', 'CIN', 'DET', 'TEN', 'NO', 'DAL', 'CHI', 'STL', 'CLE', 'HOU', 'GB', 'KC' , 'IND'):
		home_timezone[i] = 2
	if hometeam[i] == ('DEN', 'ARI'):
		home_timezone[i] = 1
for i in range(len(data)):
	if awayteam[i] in ('MIA', 'CAR', 'ATL', 'NYJ', 'BAL', 'NYG', 'NE', 'TB', 'PIT', 'WAS', 'JAC', 'PHI', 'BUF'):
		away_timezone[i] = 3
	if awayteam[i] in ('MIN', 'CIN', 'DET', 'TEN', 'NO', 'DAL', 'CHI', 'STL', 'CLE', 'HOU', 'GB', 'KC' , 'IND'):
		away_timezone[i] = 2
	if awayteam[i] == ('DEN', 'ARI'):
		away_timezone[i] = 1
time_diff = [home_timezone[i] - away_timezone[i] for i in range(len(data))]
west_east = [0]*len(data)
east_west = [0]*len(data)
for i in range(len(data)):
	if time_diff[i] == 3:
		east_west[i] = 1
	if time_diff[i] == -3:
		west_east[i] = 1
time_diff = [abs(time_diff[i]) for i in range(len(data))]
# DOME #
dome = [0]*len(data)
for i in range(len(data)):
	if hometeam[i] in ('ATL', 'MIN', 'DET', 'NO', 'DAL', 'STL', 'HOU', 'IND'):
		dome[i] = 1
	if (hometeam[i] == 'ARI') and (season[i] > 2005):
		dome[i] = 1
from datetime import datetime
for i in range(len(data)):
	date[i] = (datetime.strptime(date[i],'%Y%m%d').date())
month = [date[i].month for i in range(len(data))]
for i in range(len(data)):
	if (month[i] == 1) or (month[i] == 2):
		month[i] = 5
	if month[i] > 5:
		month[i] = (month[i]-8)
day = [date[i].weekday() for i in range(len(data))]
sunday = [0]*len(data)
for i in range(len(data)):
	if day[i] == 6:
		sunday[i] = 1
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

for i in range(len(data)):
	if (offense[i] == hometeam[i]) and (gameid[i] == gameid[i-1]):
		home_yards_gained_game[i] = (home_yards_gained_game[i-1] + yards_gained_play[i])
		away_yards_gained_game[i] = away_yards_gained_game[i-1]
	elif (offense[i] == awayteam[i]) and (gameid[i] == gameid[i-1]):
		away_yards_gained_game[i] = (away_yards_gained_game[i-1] + yards_gained_play[i])
		home_yards_gained_game[i] = home_yards_gained_game[i-1]
plays = [0]*len(data)
for i in range(len(data)):
	if i == 0:
		plays[i] = 0
	elif gameid[i] == gameid[i-1]:
		plays[i] = plays[i-1]+1
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
penalties = [0]*len(data)
for i in range(len(data)):
	if (penalty[i] == 1) and (gameid[i] == gameid[i-1]):
		penalties[i] = penalties[i-1]+1
	elif gameid[i] == gameid[i-1]:
		penalties[i] = penalties[i-1]
penalty_yards_game = [0]*len(data)
for i in range(len(data)):
	if (penalty[i] == 1) and (gameid[i] == gameid[i-1]):
		penalty_yards_game[i] = penalty_yards_game[i-1]+penalty_yards[i]
	elif gameid[i] == gameid[i-1]:
		penalty_yards_game[i] = penalty_yards_game[i-1]

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
"""		
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
"""
turnovers = [0]*len(data)
for i in range(len(data)):
	if (interception[i] == 1) or (fumble[i] == 1) and gameid[i] == gameid[i-1]:
		turnovers[i] = turnovers[i-1]+1
	elif gameid[i] == gameid[i-1]:
		turnovers[i] = turnovers[i-1]

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
total_score = [awayscore[i]+homescore[i] for i in range(len(data))]
#home_ppg = [0]*len(data)
#away_ppg = [0]*len(data)

#identifying winner
homewins = [0]*len(data)
for i in range(len(data)):
	if homescore[i] > awayscore[i]:
		homewins[i] = 1
	if homescore[i] == awayscore[i]:
		homewins[i] = 0.5
#home team margin of victory
homediff = [homescore[i] - awayscore[i] for i in range(len(data))]
"""
#Calculate seconds per play
minutes = list(data['min'])
seconds = list(data['sec'])
for i in range(len(data)):
	if seconds[i] == '**':
		seconds[i] = seconds[i-1]
for i in range(len(data)):
	if type(minutes[i]) != str and type(seconds[i]) != str:
		Seconds_Left[i] = (minutes[i]*60 + seconds[i])
	else:
		Seconds_Left[i] == Seconds_Left[i-1]
Seconds_Left = [(minutes[i]*60 + seconds[i]) for i in range(len(data))]
Seconds_Taken = Seconds_Left
for i in range(len(data)-1):
	if gameid[i] == gameid[i+1]:
		Seconds_Taken[i] = (Seconds_Left[i] - Seconds_Left[i+1])

#Calculate running time of possession		
Home_TOP = [0]*len(data)
Away_TOP = [0]*len(data)
for i in range(len(data)):
	if (offense[i] == hometeam[i]) and (gameid[i] == gameid[i-1]):
		Home_TOP[i] = (Home_TOP[i-1] + Seconds_Taken[i])
	elif (offense[i] == awayteam[i]) and (gameid[i] == gameid[i-1]):
		Away_TOP[i] = (Away_TOP[i-1] + Seconds_Taken[i])
	else:
		Away_TOP[i] = Away_TOP[i-1]
		Home_TOP[i] = Home_TOP[i-1]
TOP_diff = [Home_TOP[i] - Away_TOP[i] for i in range(len(data))]
"""		
#Play type per game
home_run = [0]*len(data)
home_pass = [0]*len(data)
home_kick = [0]*len(data)
home_punt = [0]*len(data)
away_run = [0]*len(data)
away_pass = [0]*len(data)
away_kick = [0]*len(data)
away_punt = [0]*len(data)
final_play = [0]*len(data)
for i in range(len(data)-1):
	if gameid[i] != gameid[i+1]:
		final_play[i] = 1
final_play[-1] = 1

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

# PREDICTING WINNER #	
nfldata = pd.DataFrame({'east_west':east_west, 'west_east':west_east, 'dome':dome, 'month':month, 'sunday':sunday, 'home_yards_gained_game':home_yards_gained_game, 'season':season,'away_yards_gained_game':away_yards_gained_game, 'plays':plays, 'penalties':penalties, 'penalty_yards_game':penalty_yards_game, 'turnovers':turnovers, 'home_run': home_run, 'home_pass':home_pass, 'home_kick':home_kick, 'home_punt':home_punt, 'away_run':away_run, 'away_pass':away_pass, 'away_kick':away_kick, 'away_punt':away_punt,  'total_score':total_score, 'playoffs':playoffs, 'final_play':final_play, 'homewins':homewins})
nfldata = pd.DataFrame(nfldata[~(nfldata.final_play==0)])
nfldata = pd.DataFrame(nfldata[~(nfldata.homewins == 0.5)])
nfltarget = nfldata.homewins
del nfldata['final_play'] 
del nfldata['homewins'] 
del nfldata['total_score']

from sklearn.neighbors import KNeighborsClassifier
split = 0.7
n = 200
m = 10
knn = KNeighborsClassifier(n_neighbors = m)
samplesize = len(nfldata)
n_fold_accuracy = []
final_accuracy = []
for k in range(1,m):
	for i in range(n):
		knn = KNeighborsClassifier(n_neighbors = m)
		rows = random.sample(nfldata.index, int(round(split*samplesize)))
		nfldata_train = nfldata.ix[rows]
		nfldata_test = nfldata.drop(rows)
		nfltarget_train = nfltarget.ix[rows]
		nfltarget_test = nfltarget.drop(rows)
		model= knn.fit(nfldata_train, nfltarget_train)
		x = list(knn.predict(nfldata_test))
		y = list(nfltarget_test)
		correct = [0]*len(nfldata_test)
		for j in range(len(nfldata_test)):
			if x[j] == y[j]:
				correct[j] = 1
		win_accuracy = (sum(correct)/float(len(correct)))
		n_fold_accuracy.append(win_accuracy)
		accuracy = sum(n_fold_accuracy)/float(len(n_fold_accuracy))
	final_accuracy.append(accuracy)
	
final_accuracy

pl.plot(final_accuracy)
pl.xlabel("# of Neighbors")
pl.ylabel("Percent Accuracy")
pl.title("Picking Winners with KNN cross-validation")
pl.show()

# PREDICTING POINTS #
nfldata1 = pd.DataFrame({'east_west':east_west, 'west_east':west_east, 'dome':dome, 'month':month, 'sunday':sunday, 'home_yards_gained_game':home_yards_gained_game, 'season':season,'away_yards_gained_game':away_yards_gained_game, 'plays':plays, 'penalties':penalties, 'penalty_yards_game':penalty_yards_game, 'turnovers':turnovers, 'home_run': home_run, 'home_pass':home_pass, 'home_kick':home_kick, 'home_punt':home_punt, 'away_run':away_run, 'away_pass':away_pass, 'away_kick':away_kick, 'away_punt':away_punt,  'total_score':total_score, 'playoffs':playoffs, 'final_play':final_play, 'homewins':homewins})
nfldata1 = pd.DataFrame(nfldata1[~(nfldata1.final_play==0)])
nfldata1 = pd.DataFrame(nfldata1[~(nfldata1.homewins == 0.5)])
nfltarget1 = pd.DataFrame(nfldata1.total_score)
del nfldata1['final_play'] 
del nfldata1['homewins'] 
del nfldata1['total_score']
del nfldata1['month']
del nfldata1['playoffs']
del nfldata1['west_east']
del nfldata1['east_west']
del nfldata1['sunday']

n_fold_percent_error = []
for i in range(0,n):
	rows = random.sample(nfldata1.index, int(round(split*samplesize)))
	nfldata1_train = np.array(nfldata1.ix[rows])
	nfldata1_test = np.array(nfldata1.drop(rows))
	nfltarget1_train = np.array(nfltarget1.ix[rows])
	nfltarget1_test = np.array(nfltarget1.drop(rows))
	results = sm.OLS(nfltarget1_train, nfldata1_train).fit()
	#results.summary()
	x1 = results.predict(nfldata1_test)
	y1 = nfltarget1_test
	points_accuracy = [x1[i]-y1[i] for i in range(len(nfldata1_test))]
	#pl.scatter(points_accuracy, x1)
	#pl.xlabel("Residuals")
	#pl.ylabel("Fitted Values")
	#pl.title("Residuals vs. Fitted")
	#pl.show()
	for i in range(len(points_accuracy)):
		if points_accuracy[i] < 0:
			points_accuracy[i] = points_accuracy[i]*-1
	
	avg_pts_off = sum(points_accuracy)/float(len(points_accuracy))
	avg_pts = sum(total_score)/float(len(total_score))
	percent_error = avg_pts_off / avg_pts
	n_fold_percent_error.append(percent_error)

final_percent_error = sum(n_fold_percent_error)/float(len(n_fold_percent_error))
final_percent_error
# Plot predicted vs. actual values #
pl.scatter(x1,y1)
pl.xlabel("Predicted Values")
pl.ylabel("Actual Values")
pl.title("Predicting Total Points")
pl.show()
	

# IDENTIFYING LAST PLAY OF GAME
#final_plays = pd.DataFrame()
#for i in range(len(data)-1):
#	if gameid[i] != gameid[i+1]:
#		final_plays.append(data.ix[i])
#final_plays.append(data.ix[len(data)-1])

###  grouped_data_game = data.groupby('gameid')  ###
###  grouped_data.tail(1)['offscore'] = offense's score at the end of each game  ###
###  grouped_data['ydline'].max() = the longest yards to go for either team in a given game  ###			
