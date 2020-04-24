import pandas as pd
from datetime import *
import datetime
import numpy as np


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


def parse_csv(filename):
    d = pd.read_csv(filename)
    df = pd.DataFrame(data=d)
    df['date'] = df.apply(
        lambda row: convert_date(row['tourney_date']), axis=1
    )
    return df




