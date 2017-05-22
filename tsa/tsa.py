#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bowtie.visual import Plotly

from bowtie.control import Switch, Slider, Dropdown

import numpy as np
import plotlywrapper as pw
import pandas as pd

barc = Plotly()
timeline = Plotly()

mode = Switch(caption='Airline/Airport')
mapview = Switch(caption='Map')
ddown = Dropdown(multi=True)
slide = Slider(start=5, minimum=5, maximum=100)

df = pd.read_pickle('tsa.pkl')
latlon = pd.read_csv('latlong.csv').set_index('locationID')


def load():
    vals = df['Airport Name'].unique().tolist()
    ddown.do_options(values=vals, labels=vals)
    xx = df['Airport Name'].value_counts()
    chart = xx[:5].plotly.bar()

    barc.do_all(chart.dict)



def plot(onoff, mapview, slid):

    if onoff:
        xx = df['Airline Name'].value_counts()
        vals = df['Airline Name'].unique().tolist()
        ddown.do_options(values=vals, labels=vals)
        chart = xx[:slid].plotly.bar()
    else:
        if mapview:
            xx = df['Airport Code'].value_counts()
            xx = xx[:slid]
            lls = latlon.loc[xx.index.values]
            chart = pw.scattergeo(lls.Latitude.values, -lls.Longitude.values,
                                  text=xx.index.values, size=np.sqrt(xx.values) / 5)
        else:
            xx = df['Airport Name'].value_counts()
            chart = xx[:slid].plotly.bar()
        vals = df['Airport Name'].unique().tolist()
        ddown.do_options(values=vals, labels=vals)

    barc.do_all(chart.dict)


def pevents(point):
    print(point)
    onoff = mode.get()
    if onoff:
        xx = df[df['Airline Name'] == point['x']]
        label = point['x']
    else:
        mapv = mapview.get()
        if mapv:
            xx = df[df['Airport Code'] == point['hover']]
        else:
            xx = df[df['Airport Name'] == point['x']]
        label = xx.iloc[0]['Airport Name']

    y = xx['Incident Date'].dropna()
    chart = pw.line(pd.to_datetime(y.values), np.arange(y.shape[0]), label=label)
    chart.legend()
    print(xx['Incident Date'].dtype)
    chart.data[0]['marker'] = dict(opacity=0.1)
    timeline.do_all(chart.dict)


def devents(items):
    onoff = mode.get()
    if onoff:
        q = 'Airline Name'
    else:
        q = 'Airport Name'

    chart = pw.Chart()

    for i, itm in enumerate(items):
        xx = df[df[q] == itm['value']]
        y = xx['Incident Date'].dropna()
        chart += pw.line(pd.to_datetime(y.values), np.arange(y.shape[0]), label=itm['value'])
        chart.data[i]['marker'] = dict(opacity=0.1)
    timeline.do_all(chart.dict)


from bowtie import command, Layout
@command
def build():
    layout = Layout(debug=True, rows=2)
    layout.add_sidebar(mode)
    layout.add_sidebar(mapview)
    layout.add_sidebar(slide)
    layout.add_sidebar(ddown)
    layout.add(barc)
    layout.add(timeline)

    layout.load(load)
    layout.subscribe(plot, mode.on_switch, mapview.on_switch, slide.on_change)
    layout.subscribe(pevents, barc.on_click)
    layout.subscribe(devents, ddown.on_change)
    layout.build()
