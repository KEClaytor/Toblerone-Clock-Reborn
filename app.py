from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models import ColorPicker, TextInput
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.events import DoubleTap, Tap

import numpy as np

import core

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

# UI elements
text_selected_index = TextInput(value="[]", title="Selected Index:")

# Plot
p = figure(plot_width=600, plot_height=400, x_range=(-6, 6), y_range=(-4, 4),)

p.patches(xs="xs", ys="ys", fill_color="colors", source=source)

# Switch the colors of the clicked location
def callback(event):
    indx = np.argmin((x0 - event.x) ** 2 + (y0 - event.y) ** 2)
    selected[indx] = not selected[indx]
    colors = np.array([""] * len(x0), dtype=object)
    colors[~selected] = "black"
    colors[selected] = "orange"
    print(colors)
    # We have to replace the data to refresh the plot
    # There may be a more efficient "patch" method, but it's not working for me
    source.data["colors"] = colors.tolist()
    # Update the UI
    text_selected_index.value = str(np.where(selected)[0].tolist())


p.on_event(Tap, callback)

ui = column([text_selected_index])

layout = column([ui, p])

curdoc().add_root(layout)
