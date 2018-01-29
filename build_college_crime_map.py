#!/usr/bin/env python

import plotly
plotly.tools.set_credentials_file(username='ddewitz',
                                  api_key='0UJR1yePEy3DEI3Z3grC')

import pandas as pd
import geocoder
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
import plotly.tools as tls
from standardize_crime_rate import standardize_crime_rates, get_hover_text

# set online credentials
plotly.tools.set_credentials_file(username='ddewitz',
                                  api_key='0UJR1yePEy3DEI3Z3grC')


def main():
    # load cleaned data set
    crime_df = pd.read_csv('/home/dan/Desktop/portfolio/College_Crime_Map/College_Crime_Map/data/colleges_lat_long_program.csv')
    crime_list = ['RAPE15', 'FONDL15', 'ROBBE15', 'AGG_A15']

    standardized__df = standardize_crime_rates(crime_df, crime_list)

    final_data = get_hover_text(standardized__df, crime_list)

    make_usa_crime_mape(final_data)



def make_usa_crime_mape(df):

    crime_list = ['Rape', 'Fondling', 'Robbery', 'Assault']
    count_columes = ['RAPE15', 'FONDL15', 'ROBBE15', 'AGG_A15']

    crime_traces = []
    scale = 5000

    # grouping category
    limits = crime_list
    # colors = ["rgb(116,97,26)","rgb(233,194,125)","rgb(128,205,193)","rgb(1,133,113)"]
    # colors = ["rgb(27,158,119)","rgb(217,95,2)","rgb(117,112,179)","rgb(231,41,138)"]
    # colors = ["rgb(31,120,180)","rgb(166,206,227)","rgb(178,223,138)","rgb(51,160,44)"]
    colors = ["rgb(116,97,26)","rgb(233,194,125)","rgb(166,206,227)","rgb(31,120,180)"]

    for i in range(len(limits)):

        # get school code
        lim = limits[i]

        if lim == 'Rape':
            hover_text = 'RAPE15_hover_text'
            opacity_attr = 1

        if lim == 'Fondling':
            hover_text = 'FONDL15_hover_text'
            opacity_attr = 0.9

        if lim == 'Robbery':
            hover_text = 'ROBBE15_hover_text'
            opacity_attr = 0.6

        if lim == 'Assault':
            hover_text = 'AGG_A15_hover_text'
            opacity_attr = 0.6

        # subset df where school equals sector cd
        df_sub = df[['INSTNM', 'lat', 'long', lim, hover_text]]
        df_sub.to_csv('/home/dan/Desktop/portfolio/College_Crime_Map/hover_text_TEST.csv')


        # get code definition
        type_of_crime = limits[i]

        crime = dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = df_sub["long"],
            lat = df_sub["lat"],
            text = df_sub[hover_text],
            opacity = opacity_attr,
            name = type_of_crime,
            hoverinfo = "text" + "name",
            marker = dict(
                size = df_sub[lim] * 20,
                color = colors[i],
                line = dict(width=0.5, color='rgb(40,40,40)'),
                sizemode = 'area'
                ),
            )
        crime_traces.append(crime)

    layout = dict(
        title = '<b>On Campus College Crime in 2015</b><br>bubbles display standardized crime rate per 1,000 students<br>(click legend to toggle crimes)<br>',
        showlegend = True,
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        ),
    )

    fig = dict( data=crime_traces, layout=layout )

    offline.plot(fig, filename='map_crimeLegend.html')
    # tls.get_embed('https://plot.ly/~ddewitz/69')

    # plot to my portfolio
    # py.plot(fig, filename='colle_crime_map.html')


if __name__ == "__main__":
    main()
