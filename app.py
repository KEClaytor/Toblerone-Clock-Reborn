import random
import datetime

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models import Panel, Tabs
from bokeh.models import TextInput, ColorPicker, Button, RadioButtonGroup, Select
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.events import Tap
from bokeh.palettes import Turbo256

import numpy as np

import core
import characters
import pride

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

# UI elements - Animation page
animation_radio = RadioButtonGroup(labels=["rainbow", "raindrops", "chevrons"], active=0)

# UI elements - Pride page
pride_select = Select(title="Flag", options=list(pride.flags.keys()))

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
    elif tabs.active == 4:
        # ==== Animations ====
        pass
    elif tabs.active == 5:
        # ==== Pride Flags ====
        pass
    # We have to replace the data to refresh the plot
    # There may be a more efficient "patch" method, but it's not working for me
    source.data["colors"] = colors.tolist()


def clock():
    dt = datetime.datetime.now()
    if tabs.active == 2:
        colors = characters.clock(dt.hour, dt.minute, dt.second)
        source.data["colors"] = colors.tolist()


rainbow_index = 0
raindrops = [(0, 0, 0), (-2, -2, 3), (2, 2, 5)]
def rainbow():
    if tabs.active == 3:
        if animation_radio.active == 0:
            # RAINBOW
            global rainbow_index
            colors = np.array(["black"] * 126, dtype=object)
            for shift in range(-6, 18, 2):
                c = Turbo256[(rainbow_index * 2 + shift * 10) % 256]
                for ii in core.shift(characters.diagonal, shift):
                    colors[ii] = c
            source.data["colors"] = colors.tolist()
            rainbow_index += 1
        elif animation_radio.active == 1:
            # RAINDROPS
            global raindrops
            # Update radius
            raindrops = [(x, y, r + 0.5) for (x, y, r) in raindrops]
            # Update plot
            colors = characters.ripple(x0, y0, 215, raindrops)
            source.data["colors"] = colors
            # Cull large raindrops
            raindrops = [r for r in raindrops if r[2] < 14]
            # Add new raindrops
            if len(raindrops) < 3:
                x = random.uniform(-6, 6)
                y = random.uniform(-2.5, 2.5)
                r = 0
                raindrops.append((x, y, r))
            pass
        elif animation_radio.active == 2:
            # CHEVRONS
            pass


def set_flag(attr, old, new):
    colors = pride.flag(pride_select.value)
    source.data["colors"] = colors.tolist()


p.on_event(Tap, callback)
char_button.on_click(reset)
color_button.on_click(reset)
pride_select.on_change('value', set_flag)

layout_char = column([char_button, char_text])
tab_char_designer = Panel(child=layout_char, title="Index Designer")

layout_color = column([color_button, color_text, color_picker])
tab_color_designer = Panel(child=layout_color, title="Color Designer")

tab_timer_demo = Panel(child=column([]), title="Clock Demo")

tab_animation = Panel(child=column([animation_radio]), title="Animations")

tab_pride = Panel(child=column([pride_select]), title="Pride Flags")

tabs = Tabs(tabs=[tab_char_designer, tab_color_designer, tab_timer_demo, tab_animation, tab_pride], max_width=1200)

layout = column([tabs, p])

curdoc().add_periodic_callback(clock, 100)
curdoc().add_periodic_callback(rainbow, 100)
curdoc().add_root(layout)
