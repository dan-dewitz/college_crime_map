#!/usr/bin/env python

import os, sys, inspect
import pandas as pd
# simple Google geocoding client
import geocoder
# custom module
import unit_tests

def custom_geocoder(df, column_name, write=False):
    '''get lat long coordinates from school street address

    Args:
        df: a dataframe
        column_name (str): addresses to geocode
        write (bol): True, write out csv to examine
                     addresses that failed the geocoder

    return:
        input df with additional columns for lat and long

    Google client returns lat/long tuple, tuple is parsed into
    two seperate columns -- input df, with all columns,
    is returned with additional lat long columns.
    '''
    crime_df = df

    # ----------------------------------------
    # Send address to Google Geocoing client
    # ----------------------------------------
    # applying get_lat_lng function, which calls the Google geocoder,
    # to every value in the address column
    crime_df["lat_lng"] = crime_df[column_name].apply(get_lat_lng)

    if write:
        ### print out addresses that fail the geocoder for examination
        crime_df = crime_df.fillna('')
        bad_addresses = crime_df[crime_df.lat_lng == '']

        # write for QA
        out_name = 'interation1_very_very_bad_addresses.csv'
        folder = '/output/'
        out_path = get_path() + folder + out_name
        bad_addresses.to_csv(out_path, sep=',')

    ### only keep addresses that pass the geocoder
    clean_crime_df = crime_df[crime_df.lat_lng != '']
    # out_name = 'very_good_addresses.csv'
    # folder = '/output/'
    # out_path = get_path() + folder + out_name
    # clean_crime_df.to_csv(out_path, sep=',')

    # ------
    # need this, but fuck this
    # ------
    # total address that entered geocoder = addresses that pass + addresses that fail
    unit_tests.exclusion_test(df_test=crime_df, df_inclusion=clean_crime_df,
                                                             df_exclusion=bad_addresses)

    ### split lat long tuple returned from the Google geocoder
    # into seperate columns in the df
    split_df = split_lat_lng(clean_crime_df)

    # I should not be dropping any rows on the split
    unit_tests.compare_row_counts(df_new=split_df, df_test=clean_crime_df)

    return split_df


def get_lat_lng(address):
    '''
    function takes an address as a string
    requests lat long from google geocoding client
    returns lat long as tuple
    nulls are returned as a blank string
    '''
    print "Getting lat long for .... "
    print address

    if pd.isnull(address) == True:
        print "I am null!"
        address = ''

    # request lat long from google client
    g = geocoder.google(address)

    if g.latlng is None:
        print("FUCK!!")
        print(g)

    if g.latlng is not None:
        print("good g")
        print(len(g.latlng))

        if len(g.latlng) > 2:
            print(len(g.latlng))
            print(g.latlng)
            print("What the heck!!!!")

    lat_lng = g.latlng

    return lat_lng


def split_lat_lng(df):
    '''
    splitting a tuple into two seperate columns of a dateframe
    put column names in a list, loop through list, index tuple
    by index in for loop, name column with list name
    '''
    lat_lng_list = ['lat', 'long']
    for i, col in enumerate(lat_lng_list):
        df[col] = df["lat_lng"].apply(lambda lat_lng: lat_lng[i])

    return df


def get_path():
    # simple dynamic file path
    pathname = os.path.dirname(sys.argv[0])
    abs_path = os.path.abspath(pathname)

    return abs_path


if __name__ == "__main__":
    print("module not intended to be target of execution")
