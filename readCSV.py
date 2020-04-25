import pandas as pd
from datetime import *
import datetime
import numpy as np


filename = 'ATP.csv'


def convert_date(data):
    d = str(data)
    year = int(d[0:4])
    month = int(d[5:6])
    day = int(d[7:8])
    if month < 1 or month > 12:
        return np.nan
    if day < 1 or day > 31:
        return np.nan
    parsed_date = datetime.datetime(year, month, day)
    return parsed_date


def parse_csv():
    d = pd.read_csv(filename)
    df = pd.DataFrame(data=d)
    df['date'] = df.apply(
        lambda row: convert_date(row['tourney_date']), axis=1
    )
    return df


# clean Nan values
def clean_df():
    df = parse_csv()
    df = df[['loser_age', 'loser_hand', 'loser_ht', 'loser_id', 'loser_name', 'loser_rank',
             'surface', 'date', 'tourney_level', 'tourney_name',
             'winner_age', 'winner_hand', 'winner_ht', 'winner_id', 'winner_name', 'winner_rank'
             ]]
    new_df = df.dropna(subset=['date', 'surface', 'tourney_level', 'tourney_name',
                               'loser_age', 'loser_hand', 'loser_ht', 'loser_id', 'loser_name', 'loser_rank',
                               'winner_age', 'winner_hand', 'winner_ht', 'winner_id', 'winner_name', 'winner_rank'
                               ])
    # dummies: entry, hand, name, surface, date, level, tourney name
    new_df.index = range(len(new_df))
    return new_df


def final_df():
    df = clean_df()
    return df
