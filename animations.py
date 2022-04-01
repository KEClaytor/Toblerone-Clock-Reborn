"""Animations

Repeatedly call each function for a new frame of the animation.
"""

import colorsys
import datetime

import numpy as np

# from bokeh.palettes import Turbo256

import core
import characters

# Edge elements for updating the hours
hour_index = characters.chevron_left + core.shift(characters.chevron_right, 16)
clock_colors = (characters.COLOR_WHITE, characters.COLOR_ORANGE, characters.COLOR_BLUE)

def clock_face(dt, colors=clock_colors):
    """Return the color list for a given datetime.
    """
    H, M, S = dt.hour, dt.minute, dt.second
    COL_H, COL_M, COL_S = clock_colors
    selected = np.zeros((characters.num_pixels,), dtype=bool)
    colors = [characters.COLOR_BLACK] * characters.num_pixels

    # Hours - fill the edges
    for ii, indx in enumerate(hour_index):
        if ii < H:
            colors[indx] = COL_H
    # Prevent second dots from entering hour triangles
    selected[hour_index] = True

    # Minutes - numbers in the middle
    m_tens = M // 10
    m_ones = M % 10
    for ii in core.shift(characters.digits[m_tens], 2):
        colors[ii] = COL_M
        selected[ii] = True
    for ii in core.shift(characters.digits[m_ones], 10):
        colors[ii] = COL_M
        selected[ii] = True

    # Seconds - fill in the remaining space
    for ii in range(S):
        available = np.where(~selected)[0]
        if len(available):
            indx = available[np.random.randint(len(available))]
            colors[indx] = COL_S
            selected[indx] = True

    return colors


def clamp(value, minimum=0, maximum=1):
    """Clamp a value to a max/min range.
    """
    return max(minimum, min(value, maximum))


def shift_luminosity(hls, value):
    """Shift the luminosity of a hls color.
    """
    h, l, s = hls
    return (h, clamp(l + value), s)


def rgb_to_hex(r, g, b):
    """Convert an RGB tuple (0, 1) bound to a hex color.
    """
    return f"#{round(r*255):02x}{round(g*255):02x}{round(b*255):02x}"


def rainbow(offset):
    """Return color list for the current rainbow iteration.
    """
    # Set hue, max saturation, but zero luminosity
    colors = [characters.COLOR_BLACK] * 126
    # There are 12 diagonal slashes cycle through all colors in them
    for shift in range(-6, 18, 2):
        hue = (shift * 15 + offset) % 360
        hls = (hue / 360, 0.5, 1)
        hex = rgb_to_hex(*colorsys.hls_to_rgb(*hls))
        for ii in core.shift(characters.diagonal, shift):
            colors[ii] = hex
    return colors


def ripple(x0, y0, hue, ripples):
    """Create a wave-like ripple pattern
    x0, y0 are the coordinates of the triangle centers (numpy arrays)
    hue is the ripple hue
    ripples is a (x, y, r) tuple of the ripple center (x, y) and radius (r)
    """

    # Set hue, max saturation, but zero luminosity
    hls = [(hue / 360, 0, 1)] * len(x0)
    for x, y, r in ripples:
        for ii, (xi, yi) in enumerate(zip(x0, y0)):
            ri = np.sqrt((xi - x) ** 2 + (yi - y) ** 2)
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


# def raindrops(n_raindrops=3):
#     rainbow_index = 0
#     raindrops = [(0, 0, 0), (-2, -2, 3), (2, 2, 5)]
#     yield ripple()


def chevron_right_fade(shift, hue):
    """Three right chevrons that fade out.
    """
    hls0 = (hue / 360, 0.5, 1)
    hls1 = (hue / 360, 0.25, 1)
    hls2 = (hue / 360, 0.15, 1)
    colors = np.array([(0, 0, 0)] * 126, dtype=object)
    colors[core.shift(characters.chevron_right, shift - 0)] = [hls0]
    colors[core.shift(characters.chevron_right, shift - 2)] = [hls1]
    colors[core.shift(characters.chevron_right, shift - 4)] = [hls2]
    hls = colors.tolist()
    # Convert HLS to RGB
    rgb = [colorsys.hls_to_rgb(*ci) for ci in hls]
    # Convert RGB to HEX
    hex = [rgb_to_hex(*ci) for ci in rgb]
    return np.array(hex)
