'''Shared utilities for data cleaning.'''


import pandas as pd


class CleaningError(Exception):
    pass


WHITE, BLACK, HISPANIC, OTHER = 'WHITE,BLACK,HISPANIC,OTHER'.split(',')
RACES = [WHITE, BLACK, HISPANIC, OTHER]
RACE_RENAMES = {
    'HISPANIC OR LATINO': HISPANIC,
    'BLACK OR AFRICAN AMERICAN': BLACK,
    'ANGLO OR WHITE': WHITE,
    'ANGLO': WHITE,
    'AO': WHITE,
    'ASIAN OR PACIFIC ISLANDER': OTHER,
    'AMERICAN INDIAN OR ALASKA NATIVE': OTHER,
    'AMERICAN INDIAN OR ALASKAN NATIVE': OTHER,
}
def standardize_race(r):
    if pd.isnull(r):
        return r
    return RACE_RENAMES.get(r.upper(), r)


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
