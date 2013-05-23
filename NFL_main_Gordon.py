import csv
import pdb
import sys

import pandas as pd

import play_record as pr

data = pd.DataFrame(pd.read_csv("2002_nfl_pbp_data.csv"))

plays = []
for i in data.index:
    plays.append(pr.PlayRecord(data.ix[i]))

x = plays[0]
x.set_game()

pdb.set_trace()


    
