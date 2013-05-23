import csv
import pdb
import re
import sys

import pandas as pd
#import play_parser
from pandas import *    # 1 pandas is already here 2 * imports are confusing

import parse_gameid as pg

data = DataFrame(pd.read_csv(sys.argv[1]))

#x = play_parser.Play(data['description'])

#For PlayType function
data['play_type'] = 'run'
for i in data.index:	
	if('pass' in data['description'][i]) or ('sacked' in data['description'][i]):
		data['play_type'][i] = 'pass'
	if('punts' in data['description'][i]):
		data['play_type'][i] = 'punt'
	if('kicks' in data['description'][i]) and (data['play_type'][i] != 'pass') and (data['play_type'][i] != 'punt'):
		data['play_type'][i] = 'kick'
	
#For splitting python ID variable; haven't got it working yet
gameid = list(data['gameid'])
gamedata = [pg.parse_gameid(i) for i in gameid]
# each entry in gamedata will be a tuple, arranged date, matchup, away, home

     #play = extract_play(record)
     #thisPlay = Play(play_text)

     #record_dct = parse_record(record)
     #description = record_dct['description']

