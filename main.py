from readCSV import final_df
import sqlite3
from atp_db import save_df
from atp_db import get_data
import pandas as pd
import numpy as np
import random
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


cnx = sqlite3.connect('atp.db')
cursor = cnx.cursor()
df = final_df()
df_db = get_data()
pd.options.display.max_columns = None
pd.options.display.max_rows = None


def most_win():
    return df['winner_name'].value_counts().head()


def calculate_winrate(player, idx):
    new_df = df[['winner_name', 'loser_name']].iloc[0:idx].loc[
        (df['winner_name'] == player) | (df['loser_name'] == player)]
    total_game = len(new_df)
    total_win = len(new_df.loc[new_df['winner_name'] == player])
    if total_game == 0:
        return 0
    return total_win / total_game


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


def get_random_player(winner, loser):
    tab = [winner, loser]
    return random.choice(tab)


def define_game_won(player, winner):
    if player == winner:
        return 1
    else:
        return 0


def get_player_rank(player, winner, l_rank, w_rank):
    if player == winner:
        return w_rank
    else:
        return l_rank


def get_opponent_name(player, winner, loser):
    if player == winner:
        return loser
    else:
        return winner


def get_player_age(player, winner, l_age, w_age):
    if player == winner:
        return w_age
    else:
        return l_age


def get_player_hand(player, winner, l_hand, w_hand):
    if player == winner:
        return w_hand
    else:
        return l_hand


def get_player_winrate(player, winner, l_wr, w_wr):
    if player == winner:
        return w_wr
    else:
        return l_wr


def get_player_height(player, winner, l_ht, w_ht):
    if player == winner:
        return w_ht
    else:
        return l_ht


def create_new_df(a):
    data = a.iloc[50000:99144]
    # creation of a new column : Player (random between Winner/Loser)
    data['player'] = data.apply(
        lambda row: get_random_player(row['winner_name'], row['loser_name']), axis=1
    )
    # player_result = 0 if row['player'] didn't won, player_result = 1 if row['player'] won)
    data['player_result'] = data.apply(
        lambda row: define_game_won(row['player'], row['winner_name']), axis=1
    )
    data['player_rank'] = data.apply(
        lambda row: get_player_rank(row['player'], row['winner_name'], row['loser_rank'], row['winner_rank']), axis=1
    )
    data['player_age'] = data.apply(
        lambda row: get_player_age(row['player'], row['winner_name'], row['loser_age'], row['winner_age']), axis=1
    )
    data['player_hand'] = data.apply(
        lambda row: get_player_hand(row['player'], row['winner_name'], row['loser_hand'], row['winner_hand']), axis=1
    )
    data['player_winrate'] = data.apply(
        lambda row: get_player_winrate(row['player'], row['winner_name'], row['loser_winrate'], row['winner_winrate']),
        axis=1
    )
    data['player_height'] = data.apply(
        lambda row: get_player_height(row['player'], row['winner_name'], row['loser_ht'], row['winner_ht']), axis=1
    )
    # Create columns for opponent's stats
    data['opponent'] = data.apply(
        lambda row: get_opponent_name(row['player'], row['winner_name'], row['loser_name']), axis=1
    )
    data['opponent_rank'] = data.apply(
        lambda row: get_player_rank(row['opponent'], row['winner_name'], row['loser_rank'], row['winner_rank']), axis=1
    )
    data['opponent_age'] = data.apply(
        lambda row: get_player_age(row['opponent'], row['winner_name'], row['loser_age'], row['winner_age']), axis=1
    )
    data['opponent_hand'] = data.apply(
        lambda row: get_player_hand(row['opponent'], row['winner_name'], row['loser_hand'], row['winner_hand']), axis=1
    )
    data['opponent_winrate'] = data.apply(
        lambda row: get_player_winrate(row['opponent'], row['winner_name'], row['loser_winrate'], row['winner_winrate'])
        , axis=1
    )
    data['opponent_height'] = data.apply(
        lambda row: get_player_height(row['opponent'], row['winner_name'], row['loser_ht'], row['winner_ht']), axis=1
    )
    data_final = data[['surface', 'date', 'tourney_level',
                       'opponent_rank', 'opponent_age', 'opponent_hand', 'opponent_winrate',
                       'opponent_height'
                       , 'player_rank', 'player_age', 'player_hand', 'player_winrate', 'player_height'
                       , 'player_result'
                       ]]
    return data_final

def main():

    # 1.
    # df_2018 = get_df_2018(df_db)
    # analyse_2018(df_2018)

    # 2.
    data = create_new_df(df_db)

    # handle dummies
    cat_vars = ['surface', 'tourney_level', 'opponent_hand', 'player_hand']
    for var in cat_vars:
        cat_list = 'var' + '_' + var
        cat_list = pd.get_dummies(data[var], prefix=var)
        data1 = data.join(cat_list)
        data = data1
    data_vars = data.columns.values.tolist()
    to_keep = [i for i in data_vars if i not in cat_vars]
    data_final = data[to_keep]

    # train and test sets
    idx_2018_min = 98115
    id_2018_max = 99144
    x_axis = data_final.loc[:, data_final.columns != 'player_result']
    y_axis = data_final.loc[:, data_final.columns == 'player_result']

    x_test = x_axis.iloc[idx_2018_min:id_2018_max]

    y_test = y_axis.iloc[idx_2018_min:id_2018_max]

    x_train = x_axis.iloc[:idx_2018_min]

    y_train = y_axis.iloc[:idx_2018_min]

    model = LogisticRegression()

    model.fit(x_train, y_train)

    print("here's the score")
    model.score(x_test, y_test)


main()
