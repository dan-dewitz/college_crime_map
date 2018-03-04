#!/usr/bin/env python

import pandas as pd


def standardize_crime_rates(df, crime_list):
    '''
    calculate the crime rat, per 1,000 students, for every school
    acutual calculation happens in standardize_crime_per_thousand()
    this function applies the function that standardizes the crime
    rates to every row in the df
    '''
    stand_df = df

    for crime in crime_list:
        standardized_rate_col = 'standardized_%s_rate' % crime
        stand_df[standardized_rate_col] = df.apply(standardize_crime_per_thousand, args=(crime,), axis=1)

    return stand_df


def standardize_crime_per_thousand(row, crime):
    '''
    calculate the crime rate per 1,000 students
    crime rate is rounded to two decimal points
    '''
    standardized__rate = round((row[crime] / row['Total']) * 1000, 1)

    return standardized__rate


if __name__ == "__main__":
    main()
