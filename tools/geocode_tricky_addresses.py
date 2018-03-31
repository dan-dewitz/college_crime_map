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


def geo_code_bad_addresses():
    '''getting lat long for tricky schools

    Some schools just didn't return a lat long from the geocoder
    on the first time through. These schools required different
    combinations of institution name, and address, and city, and zip.

    This part wasn't very fun.
    '''


    # write for stardardize option
    in_name = 'failed_geo_after_5_times.csv'
    in_folder = '/output/'
    in_path = get_path() + in_folder + in_name
    to_geo_code = pd.read_csv(in_path, index_col=None)


    to_geo_code["geo_address"] = to_geo_code["INSTNM"] \
                               + ", " \
                               + to_geo_code["City"] \
                               + ", " \
                               + to_geo_code["State"]

    geo_crime_df = custom_geocode.custom_geocoder(to_geo_code,
                                                  "geo_address",
                                                  write=True)

    # ----------------------------------------------------------
    # ----------------------------------------------------------

    # standardize all crime rates for every crime and school
    # crimes getting standardized are in crime list
    crime_cols = ['AGG_A16', 'ROBBE16', 'FONDL16', 'RAPE16']
    standardized__df = standardize.standardize_crime_rates(geo_crime_df, crime_cols)

    # UNIT TEST - check for dropped rows
    unit_tests.compare_row_counts(df_new=standardized__df,
                                  df_test=geo_crime_df)

    # give df intuitive names
    renamed_df = rename_columns(standardized__df)
    # UNIT TEST - check for dropped rows
    unit_tests.compare_row_counts(df_new=renamed_df,
                                  df_test=standardized__df)

    # get text for mouse hover
    final_df = get_hover_text(renamed_df, crime_cols)
    # UNIT TEST - check for dropped rows
    unit_tests.compare_row_counts(df_new=final_df,
                                  df_test=renamed_df)

    # write for QA
    out_name = 'these_guys_are_back_from_the_dead_second.csv'
    out_folder = '/output/'
    out_path = get_path() + out_folder + out_name
    final_df.to_csv(out_path, sep=',')

    return final_df


def find_final_bad_addresses():
    # bad addresses df
    in_name = 'very_bad_addresses.csv'
    in_folder = '/output/'
    in_path = get_path() + in_folder + in_name
    df_bad = pd.read_csv(in_path, index_col=None)

    # good addresses df
    in_name = 'these_guys_are_back_from_the_dead_first.csv'
    in_folder = '/output/'
    in_path = get_path() + in_folder + in_name
    df_good = pd.read_csv(in_path, index_col=None)

    very_bad = df_bad[~df_bad['geo_address'].isin(df_good['geo_address'])]

    print("all addy")
    print(df_bad.shape)

    print("good addy")
    print(df_good.shape)

    print("need to find yet")
    print(very_bad.shape)

    # write out final bad addresses
    out_name = 'the_final_remaining_bad_schools.csv'
    out_folder = '/output/'
    out_path = get_path() + out_folder + out_name
    very_bad.to_csv(out_path, sep=',')


def concat_files():
    # df1
    in_name = 'final_geocoded_data_first.csv'
    in_folder = '/output/concat_files/'
    in_path = get_path() + in_folder + in_name
    df1 = pd.read_csv(in_path, index_col=None)

    # df2
    in_name = 'hand_standardized_data_out.csv'
    # in_folder = '/output/'
    in_path = get_path() + in_folder + in_name
    df2 = pd.read_csv(in_path, index_col=None)

    # df3
    in_name = 'passed_after_5_times.csv'
    # in_folder = '/output/'
    in_path = get_path() + in_folder + in_name
    df3 = pd.read_csv(in_path, index_col=None)

    # df4
    in_name = 'these_guys_are_back_from_the_dead_first.csv'
    # in_folder = '/output/'
    in_path = get_path() + in_folder + in_name
    df4 = pd.read_csv(in_path, index_col=None)

    # df5
    in_name = 'these_guys_are_back_from_the_dead_second.csv'
    # in_folder = '/output/'
    in_path = get_path() + in_folder + in_name
    df5 = pd.read_csv(in_path, index_col=None)

    # df6
    in_name = 'these_guys_are_good_i_guess.csv'
    # in_folder = '/output/'
    in_path = get_path() + in_folder + in_name
    df6 = pd.read_csv(in_path, index_col=None)

    print(df1.shape)
    print(df2.shape)
    print(df3.shape)
    print(df4.shape)
    print(df5.shape)
    print(df6.shape)

    final_dataset = pd.concat([df1,
                               df2,
                               df3,
                               df4,
                               df5,
                               df6]).drop_duplicates()

    # write out final bad addresses
    out_name = 'final_geocoded_data.csv'
    out_folder = '/output/'
    out_path = get_path() + out_folder + out_name
    final_dataset.to_csv(out_path, sep=',')

    return final_dataset


if __name__ == "__main__":
    concat_files()
