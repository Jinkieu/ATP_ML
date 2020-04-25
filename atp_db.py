import sqlite3
from sqlite3 import Error
from readCSV import final_df
import pandas as pd

filename = 'ATP.csv'
cnx = sqlite3.connect('atp.db')
cursor = cnx.cursor()


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def save_df(new_df):
    df = new_df
    delete_query = 'DROP TABLE data'
    cursor.execute(delete_query)
    df.to_sql(name="data", con=cnx)


def get_data():
    df = pd.read_sql('select * from data', cnx)
    df.date = pd.to_datetime(df.date)
    return df



