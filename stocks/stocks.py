#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pendulum

import pandas as pd
import numpy as np
import pandas_datareader as pbr

from bowtie import cache
from bowtie.visual import Plotly
from bowtie.control import Textbox, Button

import plotlywrapper as pw

joint = Plotly()
time = Plotly()

stock1 = Textbox()
stock2 = Textbox()
button = Button('submit')

def log_returns(df):
    return np.log(df['Close'][1:].values / df['Close'][:-1].values)

def clicked():
    st1 = stock1.get()
    st2 = stock2.get()


    joint.progress.do_active()
    joint.progress.do_percent(0)
    joint.progress.do_visible(True)

    od1 = pbr.get_data_google(st1)
    joint.progress.do_inc(30)
    od2 = pbr.get_data_google(st2)
    joint.progress.do_inc(30)

    d1 = log_returns(od1)
    d2 = log_returns(od2)

    cache.save('st1', st1)
    cache.save('d1', d1)
    joint.progress.do_inc(10)
    cache.save('st2', st2)
    cache.save('d2', d2)
    joint.progress.do_inc(10)

    chart = pw.scatter(d1, d2)
    chart.data[0]['marker'] = dict(opacity=0.2)
    chart.xlabel(st1)
    chart.ylabel(st2)
    chart.title('log returns')

    joint.progress.do_visible(False)
    joint.do_all(chart.dict)

    chart = pw.line(od1.index[1:], d1, label=st1, opacity=0.3)
    chart += pw.line(od2.index[1:], d2, label=st2, opacity=0.5)
    chart.data[0]['marker'] = dict(opacity=0.2)
    chart.data[1]['marker'] = dict(opacity=0.2)
    chart.ylabel('log return')
    time.do_all(chart.dict)


def select(points):
    nums = []
    for p in points['points']:
        nums.append(p['pointNumber'])

    idx = np.unique(nums)
    d1 = np.array(cache.load('d1'))
    d2 = np.array(cache.load('d2'))

    print(idx)
    print(idx.dtype)
    print(d1[:5])
    chart = pw.scatter(d1, d2)
    chart += pw.scatter(d1[idx], d2[idx])
    chart.data[0]['marker'] = dict(opacity=0.2)
    chart.xlabel(cache.load('st1'))
    chart.ylabel(cache.load('st2'))
    chart.title('log returns')

    joint.do_all(chart.dict)


from bowtie import Layout, command
@command
def build():
    layout = Layout(rows=2, sidebar=True, debug=False)

    # layout.rows[0].fraction(2)

    layout.add(joint)
    layout.add(time)
    layout.add_sidebar(stock1)
    layout.add_sidebar(stock2)
    layout.add_sidebar(button)

    layout.subscribe(clicked, button.on_click)

    layout.subscribe(select, time.on_select)

    layout.build()
