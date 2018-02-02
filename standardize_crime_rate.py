#!/usr/bin/env python


def standardize_crime_rates(df, crime_list):
    stand_df = df

    for crime in crime_list:
        standardized_rate_col = 'standardized_%s_rate' % crime
        stand_df[standardized_rate_col] = df.apply(standardize_crime_per_thousand, args=(crime,), axis=1)

    renamed_df = rename_columns(stand_df)

    return renamed_df


def standardize_crime_per_thousand(row, crime):
    standardized__rate = round((row[crime] / row['Total']) * 1000, 1)

    return standardized__rate


def rename_columns(df):
    renamed_df = df.rename(columns={'standardized_RAPE15_rate':'Rape',
                                    'standardized_FONDL15_rate': 'Fondling',
                                    'standardized_ROBBE15_rate':'Robbery',
                                    'standardized_AGG_A15_rate':'Assault'})

    return renamed_df


def get_hover_text(df, crime_list):
    mod_df = df

    for crime in crime_list:
        crime_hover_text = '%s_hover_text' % crime
        mod_df[crime_hover_text] = df.apply(make_hover_text, args=(crime,), axis=1)

    return mod_df


def make_hover_text(row, crime):

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
        hover_text = row['INSTNM'] + '<br>' +\
                     str.title(row['City']) + '<br>' +\
                     str(row['State']) + '<br>' +\
                     'Count: ' + str(row[crime]) + '<br>' +\
                     'Rate per 1000 students: ' + str(row[std_crime_rate]) + '<br>' +\
                     'Enrollment: ' + str(int(row['Total']))

        return hover_text


if __name__ == "__main__":
    main()
