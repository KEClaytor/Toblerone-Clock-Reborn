"""The main application

Use `bokeh serve --show` to run.
"""
import random
import datetime

import numpy as np

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models import Panel, Tabs
from bokeh.models import TextInput, ColorPicker, Button, RadioButtonGroup, Select
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.events import Tap

import core
import characters
import animations
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

def reset(event):
    """Clear the display.
    """
    selected[:] = False
    colors = np.array([""] * len(x0), dtype=object)
    colors[:] = "black"
    source.data["colors"] = colors.tolist()

def update_callback(event):
    """Update the colors based on an interaction.
    """
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
    # Write to the ColumnDataSource to update the plot
    source.data["colors"] = colors.tolist()


rainbow_index = 0
raindrops = [(0, 0, 0), (-2, -2, 3), (2, 2, 5)]
def update_periodic():
    """Update the display based on a periodic schedule.
    """
    global rainbow_index
    global raindrops
    if tabs.active == 0:
        # ==== Index Designer ====
        pass
    elif tabs.active == 1:
        # ==== Color Designer ====
        pass
    elif tabs.active == 2:
        # ==== Clock Mode ====
        dt = datetime.datetime.now()
        colors = animations.clock(dt.hour, dt.minute, dt.second)
    elif tabs.active == 3:
        # ==== Animations ====
        if animation_radio.active == 0:
            # ==== Rainbow ====
            colors = animations.rainbow(rainbow_index)
            rainbow_index += 2
        elif animation_radio.active == 1:
            # ==== Raindrops ====
            # Update radius
            raindrops = [(x, y, r + 0.5) for (x, y, r) in raindrops]
            # Cull large raindrops
            raindrops = [r for r in raindrops if r[2] < 10]
            # Add new raindrops
            if len(raindrops) < 3:
                x = random.uniform(-6, 6)
                y = random.uniform(-2.5, 2.5)
                r = 0
                raindrops.append((x, y, r))
            # Create the ripples
            colors = animations.ripple(x0, y0, 215, raindrops)
        elif animation_radio.active == 2:
            # ==== Chevrons ====
            pass
    elif tabs.active == 4:
        # ==== Pride Flags ====
        pass
    if tabs.active in [2, 3]:
        source.data["colors"] = colors.tolist()


def update_attr(attr, old, new):
    """Update the display based on a selection.
    """
    colors = pride.flag(pride_select.value)
    # Write to the ColumnDataSource to update the plot
    source.data["colors"] = colors.tolist()


# Register plot clicks
p.on_event(Tap, update_callback)
# Register resets
char_button.on_click(reset)
color_button.on_click(reset)
# Register a flag select
pride_select.on_change('value', update_attr)

# Add tab layouts
layout_char = column([char_button, char_text], width=800)
tab_char_designer = Panel(child=layout_char, title="Index Designer")

layout_color = column([color_button, color_text, color_picker], width=800)
tab_color_designer = Panel(child=layout_color, title="Color Designer")

tab_timer_demo = Panel(child=column([], width=800), title="Clock Demo")

tab_animation = Panel(child=column([animation_radio], width=800), title="Animations")

tab_pride = Panel(child=column([pride_select], width=800), title="Pride Flags",)

# Add all tabs
tabs = Tabs(tabs=[tab_char_designer, tab_color_designer, tab_timer_demo, tab_animation, tab_pride], width=800)

layout = column([tabs, p], width=800)

# Add periodic (eg; time-based) callbacks
curdoc().add_periodic_callback(update_periodic, 200)
curdoc().add_root(layout)
