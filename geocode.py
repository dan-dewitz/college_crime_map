#!/usr/bin/env python

import os, sys, inspect
import pandas as pd
import geocoder


def main():
    clean_data = wrangler()

    # geocoding is turned off in function
    geocoded_data = latlong_geocoder()


def wrangler():
    data_path = get_path() + '/data/raw_oncampuscrime131415.csv'
    crime_df_raw = pd.read_csv(data_path)

    # only keep the columns I need
    crime_df = crime_df_raw.loc[:,('INSTNM', 'BRANCH', 'Address', 'City',
                                   'State', 'ZIP', 'sector_cd', 'Sector_desc',
                                   'men_total', 'women_total', 'Total',
                                   'RAPE15', 'FONDL15', 'ROBBE15', 'AGG_A15')]

    # only keep the schools that have a crime I am mapping
    crime_df = crime_df.fillna('')
    crime_df = crime_df[(crime_df.RAPE15 > 0)
                      | (crime_df.FONDL15 > 0)
                      | (crime_df.ROBBE15 > 0)
                      | (crime_df.AGG_A15 > 0)]

    # concat address, city, state into one field
    # needed for Google geocoder
    crime_df["geo_address"] = crime_df["Address"] + " " + crime_df["City"] + ", " + crime_df["State"]

    return crime_df


def geocoder(df):
    crime_df = df
    ###-----------------------------------
    ### Send addresses to Google Geocoder
    ###-----------------------------------
    if False:
        # get_lat_lng calls geocoder client on address of interest
        crime_df["lat_lng"] = crime_df["geo_address"].apply(get_lat_lng)

        # print out addresses that fail the geocoder for examination
        crime_df = crime_df.fillna('')
        bad_addresses = crime_df[crime_df.lat_lng == '']
        bad_addresses.to_csv('/home/dan/Desktop/portfolio/College_Crime_Map/bad_addresses.csv',sep=',')

        # only addresses that pass the geocoder
        clean_crime_df = crime_df[crime_df.lat_lng != '']

        # split lat long into seperate columns in the df
        split_df = split_lat_lng(clean_crime_df)

        # print out final data for examination
        split_df.to_csv('/home/dan/Desktop/portfolio/College_Crime_Map/colleges_lat_long_program.csv',sep=',')

        return split_df


def get_lat_lng(address):
    '''
    function takes an address as a string
    requst lat long from google geocoder client
    returns lat long as tuple
    '''
    print "Getting lat long .... "
    print address

    if pd.isnull(address) == True:
        print "I am null!"
        address = ''

    # request lat long from google client
    g = geocoder.google(address)
    lat_lng = g.latlng

    return lat_lng


def get_path():
    pathname = os.path.dirname(sys.argv[0])
    abs_path = os.path.abspath(pathname)

    return abs_path


def split_lat_lng(df):
    lat_lng_list = ['lat', 'long']
    for i, col in enumerate(lat_lng_list):
        df[col] = df["lat_lng"].apply(lambda lat_lng: lat_lng[i])

    return df


def check_add_for_nan(address):
    if pd.isnull(address) == True:
        print "this is null -- geo fail!"
        print "--------------"
        print address
        print "--------------"


if __name__ == "__main__":
    main()
