#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pendulum

import pandas as pd
import numpy as np
import pandas_datareader as pbr

from bowtie.visual import Plotly
from bowtie.control import Textbox, Button

import plotlywrapper as pw

joint = Plotly()
time = Plotly()

stock1 = Textbox()
stock2 = Textbox()
button = Button('submit')

def log_returns(df):
    return np.log(df['Adj Close'][1:].values / df['Adj Close'][:-1].values)

def clicked():
    st1 = stock1.get()
    st2 = stock2.get()

    od1 = pbr.get_data_yahoo(st1)
    od2 = pbr.get_data_yahoo(st2)

    d1 = log_returns(od1)
    d2 = log_returns(od2)

    chart = pw.scatter(d1, d2)
    chart.xlabel(st1)
    chart.ylabel(st2)

    joint.do_all(chart.dict)

    chart = pw.line(od1.index[1:], d1, label=st1)
    chart += pw.line(od2.index[1:], d2, label=st2)
    time.do_all(chart.dict)


from bowtie import Layout, command
@command
def build():
    layout = Layout(rows=2, sidebar=True, debug=False)

    layout.add(joint)
    layout.add(time)
    layout.add_sidebar(stock1)
    layout.add_sidebar(stock2)
    layout.add_sidebar(button)

    layout.subscribe(clicked, button.on_click)

    layout.build()
