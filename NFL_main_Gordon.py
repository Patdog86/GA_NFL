import csv
import pandas as pd
import play_parser

data = pd.read_csv("2002_nfl_pbp_data.csv")

x = play_parser.Play(data['description'])

for row in data:
     record = row
     play = extract_play(record)
     thisPlay = Play(play_text)

     record_dct = parse_record(record)
     description = record_dct['description']

