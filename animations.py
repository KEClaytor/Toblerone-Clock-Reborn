"""Animations

Repeatedly call each function for a new frame of the animation.
"""

import random
import colorsys

import numpy as np

# from bokeh.palettes import Turbo256

import core
import characters

# Edge elements for updating the hours
hour_index = [1, 0, 20, 19, 41, 40, 63, 64, 86, 87, 107, 108,
17, 18, 38, 39, 61, 62, 85, 84, 106, 105, 125, 124]


def clock(h, m, s):
    """Return color list for the clock.
    """
    selected = np.zeros((126,), dtype=bool)
    colors = np.array(["black"] * 126, dtype=object)
    
    # Hours - fill the edges
    for ii, indx in enumerate(hour_index):
        if ii <= h:
            colors[indx] = "green"
    # Prevent second dots from entering hour triangles
    selected[hour_index] = True
    
    # Minutes - numbers in the middle
    m_tens = m // 10
    m_ones = m % 10
    for ii in core.shift(characters.digits[m_tens], 2):
        colors[ii] = "orange"
        selected[ii] = True
    for ii in core.shift(characters.digits[m_ones], 10):
        colors[ii] = "orange"
        selected[ii] = True

    # Seconds - fill in the remaining space
    for ii in range(s):
        available = np.where(~selected)[0]
        indx = available[np.random.randint(len(available))]
        colors[indx] = "blue"
        selected[indx] = True

    return colors


def clamp(value, minimum=0, maximum=1):
    """Clamp a value to a max/min range.
    """
    return max(minimum, min(value, maximum))


def rgb_to_hex(r, g, b):
    """Convert an RGB tuple (0, 1) bound to a hex color.
    """
    return f"#{round(r*255):02x}{round(g*255):02x}{round(b*255):02x}"


def rainbow(offset):
    """Return color list for the current rainbow iteration.
    """
    # Set hue, max saturation, but zero luminosity
    colors = np.array(["black"] * 126, dtype=object)
    for shift in range(-6, 18, 2):
        # There are 12 diagonal slashes cycle through all colors in them
        hue = (shift * 15 + offset) % 360
        hls = (hue/360, 0.5, 1)
        hex = rgb_to_hex(*colorsys.hls_to_rgb(*hls))
        for ii in core.shift(characters.diagonal, shift):
            colors[ii] = hex
    return np.array(colors)


def ripple(x0, y0, hue, ripples):
    """Create a wave-like ripple pattern
    x0, y0 are the coordinates of the triangle centers (numpy arrays)
    hue is the ripple hue
    ripples is a (x, y, r) tuple of the ripple center (x, y) and radius (r)
    """
    def shift_luminosity(hls, value):
        h, l, s = hls
        return (h, clamp(l + value), s)

    # Set hue, max saturation, but zero luminosity
    hls = [(hue/360, 0, 1)] * len(x0)
    for x, y, r in ripples:
        for ii, (xi, yi) in enumerate(zip(x0, y0)):
            ri = np.sqrt((xi - x)**2 + (yi - y)**2)
            delta_r = 2 - np.abs(r - ri)
            # Fall off to zero at a range of 2 from the ripple radius
            #     /\         /\
            #    /  \       /  \
            # __/    \__|__/    \__
            if delta_r < 0:
                delta_r = 0
            # Lighten this pixel (allows ripples to add)
            hls[ii] = shift_luminosity(hls[ii], delta_r / 6)
    # Convert HLS to RGB
    rgb = [colorsys.hls_to_rgb(*ci) for ci in hls]
    # Convert RGB to HEX
    hex = [rgb_to_hex(*ci) for ci in rgb]
    return np.array(hex)
