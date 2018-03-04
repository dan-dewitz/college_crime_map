#!/usr/bin/env python

import os
import sys
import inspect
import pandas as pd
import geocoder

# import custom functions from tools folder
sys.path.append("tools")
import custom_geocode
import standardize
import unit_tests


def preprocess(clean=False, standardizer=False, geocode=False):
    '''
    All data wrangling steps prior to building the map are included
    in this function.
    -- if clean == True: load pre-cleaned dataset
    -- standardizer == True: create new standardized crime rate or change hover text
    -- if geocode == True: geocode the data and create a new data set

    Lat long coordinates not included in department of Ed data set.
    Therefore, the processing of this data is a bit more involved than
    you may expect, as addresses need to be geocoded.

    Hover text for map is created in this function, as it is a
    major data wrangling step

    1. read data
    2. geocode
    3. format hover text
    '''
    if clean:
        # if you just want to load the final data set from csv
        # find and return the clean data set located in the data folder
        in_name = 'final_standardized_data.csv'
        folder = '/data/'
        data_path = get_path() + folder + in_name

        # read csv into memory and check for dropped rows
        crime_df_clean = pd.read_csv(data_path, index_col=None)
        unit_tests.ut_row_count(test_df=crime_df_clean, target=1929)

        return crime_df_clean


    if standardizer:
        # if you want to adjust how crime rates are calculated
        # but not re-geocode all the data
        in_name = 'colleges_lat_long_program.csv'
        folder = '/data/'
        data_path = get_path() + folder + in_name
        crime_df_clean = pd.read_csv(data_path, index_col=None)
        unit_tests.ut_row_count(test_df=crime_df_clean, target=1929)

        # standardize all crime rates for every crime and school
        # crimes getting standardized are in crime list
        crime_cols = ['AGG_A15', 'ROBBE15', 'FONDL15', 'RAPE15']
        standardized__df = standardize.standardize_crime_rates(crime_df_clean, crime_cols)
        # UNIT TEST - check for dropped rows
        unit_tests.compare_row_counts(df_new=standardized__df,
                                           df_test=crime_df_clean)

        renamed_df = rename_columns(standardized__df)
        # UNIT TEST - check for dropped rows
        unit_tests.compare_row_counts(df_new=standardized__df,
                                           df_test=crime_df_clean)

        final_df = get_hover_text(renamed_df, crime_cols)
        # UNIT TEST - check for dropped rows
        unit_tests.compare_row_counts(df_new=standardized__df,
                                           df_test=crime_df_clean)

        # write to csv for QA
        out_name = 'final_standardized_data.csv'
        out_path = get_path() + folder + out_name
        final_df.to_csv(out_path, sep=',')

        return final_df


    if geocode:
        ### read raw data into memory
        # locate the path of execution and find the
        # data in the data folder
        in_name = 'raw_oncampuscrime131415.csv'
        folder = '/data/'
        data_path = get_path() + folder + in_name
        crime_df_raw = pd.read_csv(data_path, index_col=None)

        # UNIT TEST - check for dropped rows
        # making sure I didn't drop any rows on import
        # comparing to row count of raw csv in excel
        unit_tests.ut_row_count(test_df=crime_df_raw, target=11306)


        ### only keep the columns I need
        slim_crime_df = crime_df_raw.loc[:,('INSTNM', 'BRANCH', 'Address',
                                            'City', 'State', 'ZIP', 'sector_cd',
                                            'Sector_desc', 'men_total',
                                            'women_total', 'Total', 'RAPE15',
                                            'FONDL15', 'ROBBE15', 'AGG_A15')]

        # make complete address -- housekeeping for Google geocoder
        slim_crime_df["geo_address"] = slim_crime_df["Address"] \
                                     + " " \
                                     + slim_crime_df["City"] \
                                     + ", " \
                                     + slim_crime_df["State"]

        # UNIT TEST - check for dropped rows
        # I should still have the same number of rows as my raw data file
        unit_tests.ut_row_count(test_df=slim_crime_df, target=11306)


        ### only keep the schools that have a crime I am mapping
        # I also want to keep the number of rows under 2,500
        # which is the number of times your are allowed to hit the
        # google geocodeing server for free

        # fill na values with zeros, because I am subsetting the df by Crime > 0
        slim_crime_df.loc[:,('RAPE15','FONDL15','ROBBE15','AGG_A15')] = slim_crime_df.loc[:,('RAPE15','FONDL15',
                                                                                             'ROBBE15','AGG_A15')].fillna(value=0)
        # keep school that have a crime I am mapping
        crime_df_small = slim_crime_df[(slim_crime_df.RAPE15 > 0)
                                     | (slim_crime_df.FONDL15 > 0)
                                     | (slim_crime_df.ROBBE15 > 0)
                                     | (slim_crime_df.AGG_A15 > 0)]

        # UNIT TEST - check for poor logic and nulls
        # My exclusion set, plus my inclusion set, should equal the total
        # set prior to subsetting. Exclusion set: All crimes of interest == 0
        unit_tests.opposite_subset(df_total=slim_crime_df, df_keep=crime_df_small)


        ### Geocode / get lat long for each school of interest
        # via the google geocoder and a custom function
        # switch to True if you actually want to geocode stuff
        # unit test included in custom_geocoder
        # 'uncoded' addresses printed to data folder
        geo_crime_df = custom_geocode.custom_geocoder(crime_df_small, "geo_address")


        # standardize all crime rates for every crime and school
        # crimes getting standardized are in crime list
        crime_cols = ['AGG_A15', 'ROBBE15', 'FONDL15', 'RAPE15']
        standardized__df = standardize.standardize_crime_rates(geo_crime_df, crime_cols)

        # UNIT TEST - check for dropped rows
        unit_tests.compare_row_counts(df_new=standardized__df,
                                           df_test=geo_crime_df)

        renamed_df = rename_columns(standardized__df)
        # UNIT TEST - check for dropped rows
        unit_tests.compare_row_counts(df_new=standardized__df,
                                           df_test=crime_df_clean)

        final_df = get_hover_text(renamed_df, crime_cols)
        # UNIT TEST - check for dropped rows
        unit_tests.compare_row_counts(df_new=final_df,
                                           df_test=standardized__df)

        # write for QA
        out_name = 'final_geocoded_data.csv'
        out_path = get_path() + folder + out_name
        geo_crime_df.to_csv(out_path, sep=',')

        return geo_crime_df


def get_path():
    # simple dynamic file path
    pathname = os.path.dirname(sys.argv[0])
    abs_path = os.path.abspath(pathname)

    return abs_path


def rename_columns(df):
    # it is what it is
    renamed_df = df.rename(columns={
        'standardized_RAPE15_rate':'Rape',
        'standardized_FONDL15_rate': 'Fondling',
        'standardized_ROBBE15_rate':'Robbery',
        'standardized_AGG_A15_rate':'Assault'
        })

    return renamed_df


def get_hover_text(df, crime_list):
    # apply make_hover_text() across all the
    # rows of the df
    mod_df = df

    for crime in crime_list:
        crime_hover_text = '%s_hover_text' % crime
        # apply function across the rows of a df
        mod_df[crime_hover_text] = df.apply(make_hover_text,
                                            args=(crime,),
                                            axis=1)

    return mod_df


def make_hover_text(row, crime):
    # creating hover text for plotly map
    if crime == 'RAPE15':
        std_crime_rate = 'Rape'

    if crime == 'FONDL15':
        std_crime_rate = 'Fondling'

    if crime == 'ROBBE15':
        std_crime_rate = 'Robbery'

    if crime == 'AGG_A15':
        std_crime_rate = "Assault"

    # create hover text string
    if row['Total'] > 0:
        hover_text = row['INSTNM'] \
                       + '<br>' \
                       + str.title(row['City']) \
                       + ', ' \
                       + str(row['State']) \
                       + '<br>' \
                       + 'Crime Count: ' \
                       + str(row[crime]) \
                       + '<br>' \
                       + 'Rate per 1000 students: ' \
                       + str(row[std_crime_rate]) \
                       + '<br>' \
                       + 'Enrollment: ' \
                       + str(int(row['Total']))

        return hover_text


if __name__ == "__main__":
    preprocess(clean=True)
