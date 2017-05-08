class: title, center, middle

# Bowtie

## Interactive Dashboards

### Jacques Kvam

### 2017-05-25


---

# Agenda

--

- Motivation

--

- A quick start

--

- Advanced features

--

- How to deploy
--

- Tech stack

--

- Future work and goals

---

# Motivation

- Want to click on a chart and generate another chart.

- TODO put in two charts of a point and line graph

---

# Tool Survey

- Don't want to use R!

--

- Found them difficult to use.

--

- Thought it would be fun to write something.

---

background-image: url(standards.png)

---

# Initial Thoughts

- Plotly charts have lots of events: selection, click, and hover.

--

- Just need to communicate between Python and JS in browser.

--

- Socket.io seems like it could do the trick.

--

- That's good enough for a proof of concept.

---

class: center, middle

# Fast forward a few months

---

# Your First Bowtie App

--

### Each app has three parts

--

- Choose the components in your app.

--

- Write the callbacks: these when events trigger.

--

- Layout the components and connect everything.

---

# Define the components

These are the widgets that exist in your app.

```
from bowtie.visual import Plotly
from bowtie.control import Dropdown

plot = Plotly()
ddown = Dropdown()
```

---

# Define the callbacks

These will get called in response to JS events.
```
def callback(item):
    chart = pw.line(range(5))
    plot.do_all(chart.dict)
```

---

# Layout the App

These are the widgets that exist in your app.
```
from bowtie import command
from bowtie import Layout

@command
def build():
    layout = Layout()
    layout.add(plot)
    layout.add_sidebar(ddown)
    layout.subscribe(callback, ddown.on_select)
    layout.build()
```

---

# Advanced Features

---

# Listening to Plotly Events

---

# Subscribe to Multiple Events

---

# Take Advantage of CSS Grid

---

# Authentication

---

# Deploying

---

# Tech Stack

---


# Future Work and Goals

---

# Thanks

- To my Verdigris colleagues for feedback.

    - Danny Servén
    - Jared Kruzek
    - Martin Chang
    - Michael Roberts

- To Jeff for letting me present.

---

# Resources

- Github: `github.com/jwkvam/bowtie`

- Slides: `github.com/jwkvam/bowtie-talk`

- Docs: `bowtie-py.rtfd.io`
