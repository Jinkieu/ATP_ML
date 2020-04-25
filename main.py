from readCSV import final_df
import sqlite3
from atp_db import save_df
from atp_db import get_data

cnx = sqlite3.connect('atp.db')
cursor = cnx.cursor()
df = final_df()
df_db = get_data()


def most_win():
    return df['winner_name'].value_counts().head()


def calculate_winrate(player, idx):
    new_df = df[['winner_name', 'loser_name']].iloc[0:idx].loc[(df['winner_name'] == player) | (df['loser_name'] == player)]
    total_game = len(new_df)
    total_win = len(new_df.loc[new_df['winner_name'] == player])
    if total_game == 0:
        return 0
    return total_win/total_game


def player_winrate_before_match():
    df['winner_winrate'] = df.apply(
        lambda row: calculate_winrate(row['winner_name'], row.name), axis=1
    )
    df['loser_winrate'] = df.apply(
        lambda row: calculate_winrate(row['loser_name'], row.name), axis=1
    )
    save_df(df)


# Analysis of year 2019
def get_df_2018(df1):
    index_high = df1[df1['date'] > '2018-12-31'].index
    index_low = df1[df1['date'] < '2018-01-01'].index
    df1.drop(index_low, inplace=True)
    df1.drop(index_high, inplace=True)
    return df1


def analyse_2018(df_2018):
    df_2018.groupby()


def main():
    df_2018 = get_df_2018(df_db)
    print(df_2018['date'])


main()
