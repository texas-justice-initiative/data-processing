'''Shared utilities for data cleaning.'''


import os
import tempfile


import datadotworld as dw
import numpy as np
import pandas as pd


class CleaningError(Exception):
    pass


def upcase_strip_string_cells(df):
    for c in df.columns:
        df[c] = df[c].apply(lambda x: x if not isinstance(x, str) else x.strip().upper())


WHITE, BLACK, HISPANIC, OTHER = 'WHITE,BLACK,HISPANIC,OTHER'.split(',')
RACES = [WHITE, BLACK, HISPANIC, OTHER]


def standardize_race(race):
    if pd.isnull(race) or not race:
        return None
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


MALE = 'MALE'
FEMALE = 'FEMALE'
GENDERS_UNKNOWN = ['u']
GENDERS = [MALE, FEMALE]


def standardize_gender(gender):
    if pd.isnull(gender):
        return None
    gender = gender.strip().lower()
    if not gender:
        return None
    if gender in ('m', 'male', 'man'):
        return MALE
    elif gender in ('f', 'female', 'woman'):
        return FEMALE
    elif gender in GENDERS_UNKNOWN:
        return None
    else:
        raise CleaningError('Unrecognized gender: "%s"' % gender)


def standardize_gender_cols(df):
    cols = [c for c in df.columns if 'gender' in c.split('_') or 'sex' in c.split('_')]
    for col in cols:
        df[col] = df[col].apply(standardize_gender)


def numericalize_age_cols(df):
    cols = [c for c in df.columns if 'age' in c.split('_')]
    for c in cols:
        print("Numericalizing column %s" % c)
        bad_values = []
        new_values = []
        for value in df[c]:
            if pd.isnull(value):
                new_values.append(value)
            else:
                try:
                    newval = float(value)
                except ValueError:
                    newval = np.nan
                    bad_values.append(value)
                new_values.append(newval)
        df[c] = new_values
        df[c] = df[c].astype(float)
        if bad_values:
            print("Replaced %d bad values with NA:" % len(bad_values))
            print("Unique bad values:", set(bad_values))


def convert_date_cols(df):
    cols = [c for c in df.columns if 'date' in c.split('_')]
    cols = [c for c in cols if '_n_a' not in c and 'na' not in c.split('_')]
    for c in cols:
        print("Converting column %s to datetime" % c)
        bad_values = []
        new_values = []
        for value in df[c]:
            if pd.isnull(value):
                new_values.append(value)
            else:
                try:
                    newval = pd.to_datetime(value)
                except ValueError:
                    newval = np.nan
                    bad_values.append(value)
                new_values.append(newval)
        df[c] = new_values
        df[c] = pd.to_datetime(df[c])
        if bad_values:
            print("Replaced %d bad values with NaT:" % len(bad_values))
            print("Unique bad values:", set(bad_values))


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


def read_dtw_excel(project_key, filename):
    '''Reads a dataframe from a raw Excel file on data.world (circumventing DTW's preprocessing).'''
    datasets = dw.load_dataset(project_key, force_update=True)
    data_bytes = datasets.raw_data[filename]
    new_file, tmpfilename = tempfile.mkstemp()
    print('Writing excel file to temp file:', tmpfilename)
    os.write(new_file, data_bytes)
    os.close(new_file)
    xl = pd.ExcelFile(tmpfilename)
    sheet_names = xl.sheet_names
    if len(sheet_names) == 1:
        return xl.parse(sheet_names[0])
    return dict((name, xl.parse(name)) for name in sheet_names)



def read_dtw_csv(project_key, filename, **kwargs):
    '''Reads a dataframe from a raw CSV file on data.world (circumventing DTW's preprocessing).'''
    datasets = dw.load_dataset(project_key, force_update=True)
    data_bytes = datasets.raw_data[filename]
    new_file, tmpfilename = tempfile.mkstemp()
    print('Writing CSV to temp file:', tmpfilename)
    os.write(new_file, data_bytes)
    os.close(new_file)
    return pd.read_csv(tmpfilename, **kwargs)


def reorder_columns_and_check(df, new_order):
    '''Return dataframe with reordered columns, making sure we didn't leave any columns out.'''
    if len(new_order) != len(set(new_order)):
        raise CleaningError("Duplicate columns in new_order! Plz fix.")
    if len(df.columns) != len(set(df.columns)):
        raise CleaningError("Duplicate columns in original dataframe! Plz fix.")

    # Make sure we are only reordering columns, not dropping any
    if set(new_order) != set(df.columns):
        # At least one column exists in the old but not the new order, or vice versa.
        old_cols = list(df.columns)
        messages = []
        for c in old_cols:
            if c not in new_order:
                messages.append("Column '%s' from the original dataframe is missing in new_order" % c)
        for c in new_order:
            if c not in old_cols:
                messages.append("Column '%s' in new_order does not exist in the original dataframe" % c)
        raise CleaningError('\n'.join(messages))

    return df[new_order]
