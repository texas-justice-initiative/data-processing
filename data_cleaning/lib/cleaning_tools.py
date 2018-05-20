'''Shared utilities for data cleaning.'''


import os
import tempfile


import datadotworld as dw
import pandas as pd


class CleaningError(Exception):
    pass


def upcase_cells(df):
    for c in df.columns:
        df[c] = df[c].apply(lambda x: x if not isinstance(x, str) else x.upper())


WHITE, BLACK, HISPANIC, OTHER = 'WHITE,BLACK,HISPANIC,OTHER'.split(',')
RACES = [WHITE, BLACK, HISPANIC, OTHER]


def standardize_race(x):
    x = x.lower()
    if 'anglo' in x or 'white' in x or 'caucasian' in x or x == 'ao':
        return WHITE
    elif 'black' in x or 'african' in x:
        return BLACK
    elif (('hispanic' in x or 'latino' in x)
          and ('non hispanic' not in x)
          and ('not hispanic' not in x)):
        return HISPANIC
    else:
        return OTHER


def standardize_race_cols(df):
    cols = [c for c in df.columns if 'race' in c.split('_')]
    error_indices = set()
    for col in cols:
        df[col] = df[col].apply(standardize_race).str.upper()
        errors = df[df[col].notnull() & ~df[col].isin(RACES)]
        if len(errors):
            print('Unrecognized race(s):', ','.join(errors[col].values))
            for e in errors.index.values:
                error_indices.add(e)

    if error_indices:
        raise CleaningError("Invalid race values at indices: " + str(list(error_indices)))


def validate_gender_cols(df):
    cols = [c for c in df.columns if 'gender' in c.split('_')]
    # Check for errors in officer gender columns (values that are not 'male' nor 'female')
    error = False
    valid_genders = ('M', 'F')
    for col in cols:
        errors = df[df[col].notnull() & ~df[col].str.upper().isin(valid_genders)]
        if len(errors) > 0:
            print('Unrecognized gender(s):', ','.join(set(errors[col])))
            print('(Valid genders are: %s)' % ','.join(valid_genders))
            error = True

    if error:
        raise CleaningError("Invalid gender values, see above")


def numericalize_age_cols(df):
    # Double check that all age columns are numerical
    cols = [c for c in df.columns if 'age' in c.split('_')]
    for c in cols:
        df[c] = df[c].astype(float)


def insert_col_after(df, to_insert, name, after):
    cols = list(df.columns)
    i = cols.index(after)
    newcols = cols[:(i+1)] + [name] + cols[(i+1):]
    df[name] = to_insert
    return df[newcols]


def read_dtw_excel(project_key, filename, sheet_name=None):
    datasets = dw.load_dataset(project_key, force_update=True)
    data_bytes = datasets.raw_data[filename]
    new_file, tmpfilename = tempfile.mkstemp()
    print('Writing excel file to temp file:', tmpfilename)
    os.write(new_file, data_bytes)
    os.close(new_file)
    return pd.read_excel(tmpfilename, sheet_name=sheet_name)
