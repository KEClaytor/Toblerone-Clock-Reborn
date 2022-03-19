import colorsys

import numpy as np

from bokeh.colors import RGB

import core

digits = {
    0: [0, 1, 2, 3, 4, 19, 20, 24, 25, 41, 47, 64, 70, 86, 87, 91, 92, 107, 108, 109, 110, 111],
    1: [2, 3, 22, 23, 44, 45, 67, 68, 89, 90, 109, 110],
    2: [2, 3, 4, 21, 22, 24, 25, 46, 47, 68, 69, 89, 90, 108, 109, 110, 111, 112],
    3: [0, 1, 2, 3, 4, 23, 24, 42, 43, 44, 45, 46, 68, 69, 89, 90, 107, 108, 109],
    4: [0, 4, 19, 20, 23, 24, 40, 41, 42, 43, 44, 45, 67, 68, 89, 90, 108, 109],
    5: [0, 1, 2, 3, 4, 5, 19, 20, 41, 42, 43, 44, 45, 46, 69, 70, 91, 92, 107, 108, 109, 110, 111],
    6: [0, 1, 2, 3, 4, 19, 20, 41, 42, 43, 44, 45, 46, 64, 65, 69, 70, 86, 87, 91, 92, 107, 108, 109, 110, 111],
    7: [0, 1, 2, 3, 4, 23, 24, 44, 45, 66, 67, 87, 88, 107],
    8: [0, 1, 2, 3, 4, 20, 21, 23, 24, 43, 44, 45, 66, 67, 68, 87, 88, 90, 91, 107, 108, 109, 110, 111],
    9: [0, 1, 2, 3, 4, 19, 20, 24, 25, 41, 42, 43, 44, 45, 46, 47, 68, 69, 89, 90, 108, 109],
}

hour_index = [1, 0, 20, 19, 41, 40, 63, 64, 86, 87, 107, 108,
17, 18, 38, 39, 61, 62, 85, 84, 106, 105, 125, 124]

diagonal = [6, 7, 25, 26, 46, 47, 68, 69, 89, 90, 108, 109]
chevron_right = [1, 2, 22, 23, 45, 46, 68, 69, 89, 90, 108, 109]
chevron_left = [0, 1, 19, 20, 40, 41, 63, 64, 86, 87, 107, 108]

row_0 = list(range(19))
row_1 = list(range(19, 40))
row_2 = list(range(40, 63))
row_3 = list(range(63, 86))
row_4 = list(range(86, 107))
row_5 = list(range(107, 126))


def clock(h, m, s):
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
    m_ones = m - m_tens * 10
    for ii in core.shift(digits[m_tens], 2):
        colors[ii] = "orange"
        selected[ii] = True
    for ii in core.shift(digits[m_ones], 10):
        colors[ii] = "orange"
        selected[ii] = True

    # Seconds - fill in the remaining space
    for ii in range(s):
        available = np.where(~selected)[0]
        indx = available[np.random.randint(len(available))]
        colors[indx] = "blue"
        selected[indx] = True

    return colors


def ripple(x0, y0, hue, ripples):
    """Create a wave-like ripple pattern
    x0, y0 are the coordinates of the triangle centers (numpy arrays)
    hue is the ripple hue
    ripples is a (x, y, r) tuple of the ripple center (x, y) and radius (r)
    """
    # Zero out all colors
    colors = [RGB(*colorsys.hls_to_rgb(hue, 0, 255))] * len(x0)
    for x, y, r in ripples:
        print("Ripple:", x, y, r)
        for ii, (xi, yi) in enumerate(zip(x0, y0)):
            ri = np.sqrt((xi - x)**2 + (yi - y)**2)
            delta_r = 2 - np.abs(r - ri)
            # Fall off to zero at a range of 2 from the ripple radius
            #     /\         /\
            #    /  \       /  \
            # __/    \__|__/    \__
            if delta_r < 0:
                delta_r = 0
            # Set ripple color
            colors[ii] = colors[ii].lighten(delta_r * 0.15)
    return [c.to_hex() for c in colors]
