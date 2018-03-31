#!/usr/bin/env python

import os
import sys
import pandas as pd

#===================#
# Unit Test Library #
#===================#


def ut_row_count(test_df, target):
    '''
    simple test to be sure I am not dropping any rows when
    importing the raw csv file
    -- target is a hardcoded value, typically from a
       row count in excel or another spreadsheet tool
    '''
    test = test_df.shape
    print "row count of test df:", test[0]

    if test[0] != target:
        sys.exit("you dropped a row, buddy; failed ut_row_count(test_df, target)")
    else:
        print test[0], "==", target, "successful import!"


def opposite_subset(df_total, df_keep):
    '''
    if I am truly getting every school with a crime of interest
    in my subset. Then, the schools that remain, should not of had
    a single case for any of the crimes of interest
    '''
    print "I'm checking your exclusion set"

    total = df_total.shape
    keep = df_keep.shape

    print df_total.shape

    opp_df = df_total[(df_total.RAPE16 == 0)
                    & (df_total.FONDL16 == 0)
                    & (df_total.ROBBE16 == 0)
                    & (df_total.AGG_A16 == 0)
                    | (df_total.City == '')
                    | (df_total.State == '')
                    | (df_total.ZIP == '')]

    opp_df_count = opp_df.shape

    print "total:", total[0]
    print "keep: ", keep[0]
    print "opp_df_count:", opp_df_count[0]

    if opp_df_count[0] + keep[0] != total[0]:
        sys.exit("something is up with your subsetting; failed opposite_subset(df_total, df_keep)")
    else:
        print opp_df_count[0], "+", keep[0], "=", total[0], "successful subsetting"


def compare_row_counts(df_new, df_test):
    '''
    compare the row count of a newly created df to that
    of a test df, which most likely comes from a previous
    stage in data wrangling
    '''
    print "comparing the row counts between two dfs"

    new = df_new.shape
    test = df_test.shape

    print "new:", new[0]
    print "test: ", test[0]

    if new[0] != test[0]:
        sys.exit("you dropped a row, pal!; failed compare_row_counts(df_new, df_test)")
    else:
        print new[0], "==", test[0], " -- successful subsetting"


def exclusion_test(df_test, df_inclusion, df_exclusion):
    '''
    Checking for null or other unexpected values in the df.
    If I am correclty subsetting the data, then I should be
    to add of the row counts for the inclusion and exclusion
    datasets, to equal the total dataset prior to subsetting.
    '''
    print "comparing the row counts between two dfs"

    test = df_test.shape
    inclusion = df_inclusion.shape
    exclusion = df_exclusion.shape

    print "test: ", test[0]
    print "inclusion: ", inclusion[0]
    print "exclusion: ", exclusion[0]

    if inclusion[0] + exclusion[0] != test[0]:
        sys.exit("you are missing some values after geocoding, buddy!; failed exclusion_test(df_test, df_inclusion, df_exclusion)")
    else:
        print inclusion[0], "+", exclusion[0], "=", test[0], " -- successful subsetting"
