#!/usr/bin/env python

import plotly
import sys
import pandas as pd
import geocoder
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
import plotly.tools as tls
#custom module
import preprocess

# set online credentials for plotly
plotly.tools.set_credentials_file(username='ddewitz',
                                  api_key='0UJR1yePEy3DEI3Z3grC')


def main():
    # load cleaned data set
    crime_df = preprocess.preprocess(clean=True)
    # make the map - save html to local machine
    make_college_crime_map(crime_df, online=True)


def make_college_crime_map(df, local=False, online=False):
    '''
    create plotly bubble map
    -- if local == True: write to local html
    -- if online == True: write to Plotly portfolio
    '''
    # these are the crimes I'm mapping
    crime_list = ['Assault', 'Robbery', 'Fondling', 'Rape']
    # will append each crime, or trace, to this list
    crime_traces = []
    # grouping category
    limits = crime_list
    # set colors for crime ledgend - indexed in for loop
    colors = ["rgb(31,120,180)","rgb(166,206,227)","rgb(233,194,125)","rgb(116,97,26)"]

    for i in range(len(limits)):
        # get crime
        lim = limits[i]

        # set crime specific settings
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
        # do not show school if a crime has not occured on its campus
        df_sub = df_sub[df_sub[lim] > 0]

        crime = dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = df_sub["long"],
            lat = df_sub["lat"],
            text = df_sub[hover_text],
            opacity = opacity_attr,
            name = lim,
            marker = dict(
                size = df_sub[lim] * 20,
                color = colors[i],
                line = dict(width=0.5, color='rgb(40,40,40)'),
                sizemode = 'area'
                ),
            )
        # appended trace to list of traces
        crime_traces.append(crime)

    # the legend and annotations between the local
    # html and the more sharable plotly iframe are pretty
    # different, so that's the reason for this if statement
    if online:
        layout = dict(
            showlegend = True,
            legend = dict(
                traceorder='normal',
                orientation="h",
                x=0,
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
            ),
            annotations=[
                dict(
                      x=0.008,
                      y=0.99,
                      text="click legend to toggle crimes ~ scroll to zoom",
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
