#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pendulum

import pandas as pd
import pandas_datareader as pbr

from bowtie.visual import Plotly
from bowtie.control import Textbox, Button

import plotlywrapper as pw

joint = Plotly()

stock1 = Textbox()
stock2 = Textbox()
button = Button('submit')

def log_returns(df):
    return np.log(df['Adj Close'][1:].values / df['Adj Close'][:-1].values)

def clicked():
    st1 = stock1.get()
    st2 = stock2.get()

    d1 = pbr.get_data_yahoo(st1)
    d2 = pbr.get_data_yahoo(st2)

    chart = pw.scatter(d1, d2)
    chart.xlabel(st1)
    chart.ylabel(st2)

    joint.do_all(chart.dict)


from bowtie import Layout, command
@command
def build():
    layout = Layout(sidebar=True, debug=False)

    # layout.columns[1].pixels(100)
    # layout.rows[0].pixels(40)

    layout.add(joint)
    layout.add_sidebar(stock1)
    layout.add_sidebar(stock2)
    layout.add_sidebar(button)

    layout.subscribe(clicked, button.on_click)

    layout.build()
