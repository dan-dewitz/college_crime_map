#!/usr/bin/env python

import os, sys, inspect
import pandas as pd
# simple Google geocoding client
import geocoder
# custom module
import unit_tests

def custom_geocoder(df, column_name):
    '''
    function takes a df, subsets the df on the address column
    loops through each value in the column, sending the address to
    the Google geocoding client.
    -- the client returns a tuple
    -- tuple is parsed into two seperate columns
    -- full df is returned with additional lat long columns
    '''
    crime_df = df

    ### Send address to Google Geocoing client
    # applying get_lat_lng function, which calls the Google geocoder,
    # to every value in the address column
    crime_df["lat_lng"] = crime_df[column_name].apply(get_lat_lng)

    ### print out addresses that fail the geocoder for examination
    crime_df = crime_df.fillna('')
    bad_addresses = crime_df[crime_df.lat_lng == '']
    # write for QA
    out_name = 'bad_addresses.csv'
    folder = '/data/'
    out_path = get_path() + folder + out_name
    bad_addresses.to_csv(out_path, sep=',')

    ### only keep addresses that pass the geocoder
    clean_crime_df = crime_df[crime_df.lat_lng != '']
    out_name = 'good_addresses.csv'
    folder = '/data/'
    out_path = get_path() + folder + out_name
    bad_addresses.to_csv(out_path, sep=',')

    # total address that entered geocoder = addresses that pass + addresses that fail
    unit_tests.exclusion_test(df_test=crime_df, df_inclusion=clean_crime_df, df_exclusion=bad_addresses)

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
    custom_geocode()
