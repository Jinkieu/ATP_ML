from readCSV import final_df
import sqlite3
from atp_db import save_df
from atp_db import get_data
import pandas as pd

cnx = sqlite3.connect('atp.db')
cursor = cnx.cursor()
df = final_df()
df_db = get_data()
pd.options.display.max_columns = None
pd.options.display.max_rows = None


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
    del df_2018['index']
    del df_2018['winner_id']
    del df_2018['loser_id']
    print('Impact of surface: ')
    print(df_2018.groupby('surface').mean())
    # figures show us that the surface has an impact on the winner
    print('___________________')
    print('Impact of the tournament level: ')
    print(df_2018.groupby('tourney_level').mean())
    # figures sho us that the level of the tournament has an impact on the winner

    # analyse whether a right-handed player has a higher winrate than a southpaw
    southpaw_win = len(df_2018.loc[df_2018['winner_hand'] == 'L'])
    right_handed_win = len(df_2018.loc[df_2018['winner_hand'] == 'R'])
    total_game_with_southpaw = df_2018.loc[(df_2018['winner_hand'] == 'L') | (df_2018['loser_hand'] == 'L')]
    total_game_with_right_handed = df_2018.loc[(df_2018['winner_hand'] == 'R') | (df_2018['loser_hand'] == 'R')]
    southpaw_winrate = southpaw_win / len(total_game_with_southpaw)
    right_handed_winrate = right_handed_win / len(total_game_with_right_handed)
    print('___________________')
    print('impact of the dominant hand: ')
    print('Southpaw winrate: ', southpaw_winrate)
    print('Right-handed winrate: ', right_handed_winrate)
    # A right-handed player seems to have a better winrate than a southpaw
    # However this analysis can be biased because there are way more right-handed players than southpaws


def main():
    df_2018 = get_df_2018(df_db)
    analyse_2018(df_2018)


main()
