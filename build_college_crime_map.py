#!/usr/bin/env python

import plotly
import sys
import pandas as pd
import geocoder
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
import plotly.tools as tls
# custom module
sys.path.append("tools")
import preprocess

# set online credentials for plotly
plotly.tools.set_credentials_file(username='ddewitz',
                                  api_key='0UJR1yePEy3DEI3Z3grC')


def main():
    # load cleaned data set
    crime_df = preprocess.preprocess(clean=True)

    # make the map - save html to local machine
    make_college_crime_map(crime_df, online=True, local=True)


def make_college_crime_map(df, local=False, online=False):
    '''create plotly bubble map

    Args:
        df: clean dataset ready to map
        local: True, write to local html
        online: True, write to Plotly portfolio

    Local and Online maps also have slightly different designs,
    which is the reason for a special arg
    '''
    # these are the crimes I'm mapping
    crime_list = ['Robbery', 'Fondling', 'Assault', 'Rape']

    # will append each crime category, or trace, to this list
    crime_traces = []

    # set colors for crime ledgend - indexed in for loop
    colors = ["rgb(166,206,227)","rgb(233,194,125)","rgb(31,120,180)","rgb(116,97,26)"]

    for i, crime in enumerate(crime_list):

        # set crime specific attributes
        if crime == 'Rape':
            hover_text = 'RAPE16_hover_text'
            opacity_attr = 1

        if crime == 'Fondling':
            hover_text = 'FONDL16_hover_text'
            opacity_attr = 0.9

        if crime == 'Robbery':
            hover_text = 'ROBBE16_hover_text'
            opacity_attr = 0.6

        if crime == 'Assault':
            hover_text = 'AGG_A16_hover_text'
            opacity_attr = 0.6

        # subset df where school equals sector cd
        df_sub = df[['INSTNM', 'lat', 'long', crime, hover_text]]

        # do not show school if a crime has not occured on its campus
        df_sub = df_sub[df_sub[crime] > 0]

        crime_bubbles = dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = df_sub["long"],
            lat = df_sub["lat"],
            text = df_sub[hover_text],
            opacity = opacity_attr,
            name = crime,
            marker = dict(
                size = df_sub[crime] * 20,
                color = colors[i],
                line = dict(width=0.5, color='rgb(40,40,40)'),
                sizemode = 'area'
                ),
            )
        # appended trace to list of traces
        crime_traces.append(crime_bubbles)

    # the legend and annotations between the local
    # html and the more sharable plotly iframe are pretty
    # different, so that's the reason for this if statement
    if online:
        layout = dict(
            autosize = True,
            showlegend = True,
            legend = dict(
                traceorder='normal',
                orientation="h",
                # xanchor="left",
                # yanchor="top",
                # x=0,
                y=1.06,
                font = dict(
                    size=25
                )
            ),
            geo = dict(
                scope='usa',
                projection=dict(type='albers usa'),
                showland = True,
                landcolor = 'rgb(217, 217, 217)',
                subunitwidth=1,
                countrywidth=1,
                subunitcolor="rgb(255, 255, 255)",
                countrycolor="rgb(255, 255, 255)"
            )
        )

        # create plotly figure
        fig = dict(data=crime_traces, layout=layout)
        py.plot(fig, filename='college_crime_map.html')

    # create local version
    if local:
        layout = dict(
            showlegend = True,
            legend = dict(
                traceorder='normal',
                orientation="h",
                x=0.147,
                y=1.13
            ),
            geo = dict(
                scope='usa',
                projection=dict(type='albers usa'),
                showland = True,
                landcolor = 'rgb(217, 217, 217)',
                subunitwidth=1,
                countrywidth=1,
                subunitcolor="rgb(255, 255, 255)",
                countrycolor="rgb(255, 255, 255)"
            ),
            annotations=[
                dict(
                      x=0.155,
                      y=1.06,
                      text="click legend to toggle crimes",
                      showarrow=False,
                      font = dict(
                          family="Arial",
                          color="rgb(105,105,105)"
                      )
                )
            ]
        )

        # create plotly figure
        fig = dict(data=crime_traces, layout=layout)
        offline.plot(fig, filename='college_crime_map.html')
        # tls.get_embed('https://plot.ly/~ddewitz/69')


if __name__ == "__main__":
    main()
