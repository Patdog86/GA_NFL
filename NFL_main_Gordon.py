import csv
import pdb
import sys

import pandas as pd

import play_record as pr

data = pd.read_csv(sys.argv[1])

data = pd.DataFrame(pd.read_csv(sys.argv[1]))

plays = []
for i in data.index:
    plays.append(pr.PlayRecord(data.ix[i]))

x = plays[0]
x.set_game()

pdb.set_trace()


    
