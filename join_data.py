import os
import sys
import pandas as pd

os.chdir('..')
path = 'data/all/'


def preprocess(raw):
    cols_to_drop = ['Crime ID', 'Reported by', 'Falls within', 'LSOA code', 'LSOA name', 'Last outcome category', 'Context']
    data = raw.drop(cols_to_drop, axis=1)
    data = data.dropna()
    return data


def read_data():
    final_df = pd.DataFrame()
    for directory in os.listdir(path):
        if not directory.startswith('.'):
            folder = path + directory + '/'
            for file in os.listdir(folder):
                df = pd.read_csv(folder+file)
                final_df = final_df.append(df, ignore_index=True)
    return preprocess(final_df)


def save_data():
    data = read_data()
    data.to_csv('data/london.csv')
