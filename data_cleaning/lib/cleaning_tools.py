'''Shared utilities for data cleaning.'''


import os
import tempfile


import datadotworld as dw
import pandas as pd


class CleaningError(Exception):
    pass


def upcase_strip_string_cells(df):
    for c in df.columns:
        df[c] = df[c].apply(lambda x: x if not isinstance(x, str) else x.strip().upper())


WHITE, BLACK, HISPANIC, OTHER = 'WHITE,BLACK,HISPANIC,OTHER'.split(',')
RACES = [WHITE, BLACK, HISPANIC, OTHER]


def standardize_race(race):
    if pd.isnull(race):
        return race
    race = race.lower()
    if 'anglo' in race or 'white' in race or 'caucasian' in race or race == 'ao':
        return WHITE
    elif 'black' in race or 'african' in race:
        return BLACK
    elif (('hispanic' in race or 'latino' in race)
          and ('non hispanic' not in race)
          and ('not hispanic' not in race)):
        return HISPANIC
    else:
        return OTHER


def standardize_race_cols(df):
    cols = [c for c in df.columns if 'race' in c.split('_') or 'ethnicity' in c.split('_')]
    for col in cols:
        df[col] = df[col].apply(standardize_race)


MALE = 'M'
FEMALE = 'F'
GENDERS = [MALE, FEMALE]


def standardize_gender(gender):
    if pd.isnull(gender):
        return gender
    g = gender.lower()
    if g in ('m', 'male', 'man'):
        return MALE
    elif g in ('f', 'female', 'woman'):
        return FEMALE
    else:
        raise CleaningError('Unrecognized gender: "%s"' % gender)


def standardize_gender_cols(df):
    cols = [c for c in df.columns if 'gender' in c.split('_') or 'sex' in c.split('_')]
    for col in cols:
        df[col] = df[col].apply(standardize_gender)


def numericalize_age_cols(df):
    cols = [c for c in df.columns if 'age' in c.split('_')]
    for c in cols:
        df[c] = df[c].astype(float)


def standardize_name(name):
    if pd.isnull(name):
        return None
    name = str(name)
    parts = name.split()
    parts = [''.join(ch for ch in p if ch.isalnum() or ch == '-') for p in parts]
    name = ' '.join([p for p in parts if p])
    return name if name else None


def insert_col_after(df, to_insert, name, after):
    cols = list(df.columns)
    i = cols.index(after)
    newcols = cols[:(i+1)] + [name] + cols[(i+1):]
    df[name] = to_insert
    return df[newcols]


def read_dtw_excel(project_key, filename, sheet_names=[None]):
    '''Reads a dataframe from a raw Excel file on data.world (circumventing DTW's preprocessing).'''
    if not isinstance(sheet_names, list):
        sheet_names = [sheet_names]
    datasets = dw.load_dataset(project_key, force_update=True)
    data_bytes = datasets.raw_data[filename]
    new_file, tmpfilename = tempfile.mkstemp()
    print('Writing excel file to temp file:', tmpfilename)
    os.write(new_file, data_bytes)
    os.close(new_file)
    frames = [pd.read_excel(tmpfilename, sheet_name=sheet) for sheet in sheet_names]
    if len(frames) == 1:
        return frames[0]
    else:
        return frames
