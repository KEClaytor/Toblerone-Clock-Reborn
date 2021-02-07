import numpy as np

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


def clock(h, m, s):
    selected = np.zeros((126,), dtype=bool)
    colors = np.array(["black"] * 126, dtype=object)
    
    # Hours - fill the edges
    for ii, indx in enumerate(hour_index):
        if ii <= h:
            colors[indx] = "green"
            selected[indx] = True
    
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
