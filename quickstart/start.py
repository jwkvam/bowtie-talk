#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bowtie.visual import Plotly
from bowtie.control import Dropdown

import plotlywrapper as pw
import numpy as np


plot = Plotly()
ddown = Dropdown(labels=range(1, 6), values=range(1, 6))

def callback(item):
    t = np.linspace(0, 1, 100)
    y = np.sin(2*np.pi*item['value']*t)
    chart = pw.line(t, y)
    plot.do_all(chart.dict)


from bowtie import command
@command
def build():
    from bowtie import Layout
    layout = Layout(debug=True)
    layout.add(plot)
    layout.add_sidebar(ddown)
    layout.subscribe(callback, ddown.on_change)
    layout.build()
