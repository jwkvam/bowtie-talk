#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy.random as rng
import pandas as pd

from bowtie.visual import Plotly, Table

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

import plotlywrapper as pw

data = pd.read_csv('train.csv')

def convert(series):
    return series.astype('category').cat.codes

data.Sex = convert(data.Sex)
data.Embarked = convert(data.Embarked)

rng.seed(1)

train, test = train_test_split(data)

train.fillna(-1, inplace=True)
test.fillna(-1, inplace=True)

gbc = GradientBoostingClassifier()

features = ['Pclass', 'Sex', 'Age', 'Embarked', 'Fare', 'SibSp', 'Parch']
label = 'Survived'

gbc = gbc.fit(train[features], train[label])

train_pred = gbc.predict_proba(train[features])[:, 1]
test_pred = gbc.predict_proba(test[features])[:, 1]

train_resid = train[label] - train_pred
test_resid = test[label] - test_pred

train['pred'] = train_pred
test['pred'] = test_pred

train = train.round({'pred': 2})
test = test.round({'pred': 2})

train.drop('Ticket', axis=1, inplace=True)
test.drop('Ticket', axis=1, inplace=True)

train_plot = Plotly()
test_plot = Plotly()
table = Table(results_per_page=20)
summary = Table(results_per_page=7)


def load():
    chart = pw.scatter(train_resid)
    chart.ylim(-1, 1)
    chart.title('Train Residual')
    chart.xlabel('sample')
    chart.ylabel('true - pred')
    train_plot.do_all(chart.dict)

    chart = pw.scatter(test_resid)
    chart.ylim(-1, 1)
    chart.title('Test Residual')
    chart.xlabel('sample')
    chart.ylabel('true - pred')
    test_plot.do_all(chart.dict)


def train_select(points):
    idx = [x['pointNumber'] for x in points['points']]
    table.do_data(train.iloc[idx])
    summ = train.iloc[idx].describe().iloc[1:, 1:]
    summ = summ.round(2)
    summ = summ.reset_index()
    summary.do_data(summ)


def test_select(points):
    idx = [x['pointNumber'] for x in points['points']]
    table.do_data(test.iloc[idx])
    summ = test.iloc[idx].describe().iloc[1:, 1:]
    summ = summ.reset_index()
    summ = summ.round(2)
    summary.do_data(summ)


from bowtie import Layout, command
@command
def build():
    layout = Layout(rows=3, columns=2, sidebar=False, debug=True)

    layout.rows[0].fraction(3)
    layout.rows[1].fraction(1)
    layout.rows[2].fraction(2)
    layout.columns[1].fraction(3)

    layout.add(train_plot, 0, 0)
    layout.add(test_plot, 1, 0, 2, 0)
    layout.add(table, 0, 1, 1, 1)
    layout.add(summary, 2, 1)

    layout.subscribe(train_select, train_plot.on_select)
    layout.subscribe(test_select, test_plot.on_select)

    layout.load(load)
    layout.build()
