import datetime

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models import Panel, Tabs
from bokeh.models import TextInput, ColorPicker, Button
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.events import DoubleTap, Tap

import numpy as np

import core
import characters

# Data
(x0, y0, xs, ys) = core.extended()
source = ColumnDataSource(
    data={"x0": x0, "y0": y0, "xs": xs, "ys": ys, "colors": ["black"] * len(x0)}
)
x0 = np.array(x0)
xs = np.array(xs)
y0 = np.array(y0)
ys = np.array(ys)
selected = np.zeros(x0.shape, dtype=bool)

# UI elements - Character designer
char_button = Button(label="Reset")
char_text = TextInput(value="[]", title="Selected Index:")

# UI elements - Color picker
color_button = Button(label="Reset")
color_text = TextInput(value="[]", title="Colors:")
color_picker = ColorPicker(title="Color")

# Plot
p = figure(plot_width=600, plot_height=400, x_range=(-6, 6), y_range=(-4, 4),)

p.patches(xs="xs", ys="ys", fill_color="colors", source=source)

# Reset the array
def reset(event):
    selected[:] = False
    colors = np.array([""] * len(x0), dtype=object)
    colors[:] = "black"
    source.data["colors"] = colors.tolist()


# Switch the colors of the clicked location
def callback(event):
    colors = np.array(source.data["colors"], dtype=object)
    indx = np.argmin((x0 - event.x) ** 2 + (y0 - event.y) ** 2)
    if tabs.active == 0:
        # ==== Index Designer ====
        selected[indx] = not selected[indx]
        colors[~selected] = "black"
        colors[selected] = "orange"
        # Update the UI
        char_text.value = str(np.where(selected)[0].tolist())
    elif tabs.active == 1:
        # ==== Color Designer ====
        colors[indx] = color_picker.color
        # Update the UI
        color_text.value = str(colors.tolist())
    elif tabs.active == 2:
        # ==== Clock Mode ====
        # Update from clock()
        pass
    # We have to replace the data to refresh the plot
    # There may be a more efficient "patch" method, but it's not working for me
    source.data["colors"] = colors.tolist()


def clock():
    dt = datetime.datetime.now()
    if tabs.active == 2:
        colors = characters.clock(dt.hour, dt.minute, dt.second)
        source.data["colors"] = colors.tolist()


p.on_event(Tap, callback)
char_button.on_click(reset)
color_button.on_click(reset)

ui = column([char_text])

layout_char = column([char_button, char_text])
tab_char_designer = Panel(child=layout_char, title="Index Designer")

layout_color = column([color_button, color_text, color_picker])
tab_color_designer = Panel(child=layout_color, title="Color Designer")

tab_timer_demo = Panel(child=column([]), title="Clock Demo")

tabs = Tabs(tabs=[tab_char_designer, tab_color_designer, tab_timer_demo])

layout = column([tabs, p])

curdoc().add_periodic_callback(clock, 100)
curdoc().add_root(layout)
