#!/usr/bin/env python
# -*- coding: utf-8 -*-

from queue import Queue

import pendulum

from bowtie.control import Textbox, Button

LINES = Queue(maxsize=50)

talk = Textbox()
click = Button('submit')
chat = Textbox(autosize=True, disabled=True, area=True)

def to_text(entry):
    return f'{entry[0].diff_for_humans()}: {entry[1]}'

def update_chat():
    chat.do_text('\n'.join(map(to_text, list(LINES.queue)[::-1])))

def clicked():
    text = talk.get()
    entered(text)

def entered(text):
    if LINES.full():
        _ = LINES.get()
    tt = text[:144]
    now = pendulum.utcnow()
    LINES.put((now, tt))
    update_chat()
    talk.do_text('')

from bowtie import Layout, command
@command
def build():
    layout = Layout(rows=2, columns=2, sidebar=False, debug=False)

    layout.columns[1].pixels(100)
    layout.rows[0].pixels(40)

    layout.add(talk, row_start=0, column_start=0)
    layout.add(click, row_start=0, column_start=1)
    layout.add(chat, row_start=1, column_start=0, row_end=1, column_end=1)

    layout.load(update_chat)

    layout.subscribe(entered, talk.on_enter)
    layout.subscribe(clicked, click.on_click)
    layout.schedule(5, update_chat)

    layout.build()
