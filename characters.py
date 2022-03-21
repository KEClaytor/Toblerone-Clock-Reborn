"""Characters

Contains dictionaries for the extended layout for characters and patterns.
"""

# Numeric digits
digits = {
    0: [0, 1, 2, 3, 4, 19, 20, 24, 25, 41, 47, 64, 70, 86, 87, 91, 92, 107, 108, 109, 110, 111],
    1: [2, 3, 22, 23, 44, 45, 67, 68, 89, 90, 109, 110],
    2: [2, 3, 4, 21, 22, 24, 25, 46, 47, 68, 69, 89, 90, 108, 109, 110, 111, 112],
    3: [0, 1, 2, 3, 4, 23, 24, 42, 43, 44, 45, 46, 68, 69, 89, 90, 107, 108, 109],
    4: [0, 1, 4, 19, 20, 23, 24, 41, 42, 43, 44, 45, 67, 68, 89, 90, 109],
    5: [0, 1, 2, 3, 4, 5, 19, 20, 41, 42, 43, 44, 45, 46, 69, 70, 91, 92, 107, 108, 109, 110, 111],
    6: [0, 1, 2, 3, 4, 19, 20, 41, 42, 43, 44, 45, 46, 64, 65, 69, 70, 86, 87, 91, 92, 107, 108, 109, 110, 111],
    7: [0, 1, 2, 3, 4, 23, 24, 44, 45, 66, 67, 87, 88, 107],
    8: [0, 1, 2, 3, 4, 20, 21, 23, 24, 43, 44, 45, 66, 67, 68, 87, 88, 90, 91, 107, 108, 109, 110, 111],
    9: [0, 1, 2, 3, 4, 19, 20, 24, 25, 41, 42, 43, 44, 45, 46, 47, 68, 69, 89, 90, 108, 109],
}

# Patterns
diagonal = [6, 7, 25, 26, 46, 47, 68, 69, 89, 90, 108, 109]
chevron_right = [1, 2, 22, 23, 45, 46, 68, 69, 89, 90, 108, 109]
chevron_left = [0, 1, 19, 20, 40, 41, 63, 64, 86, 87, 107, 108]

# Rows
row_0 = list(range(19))
row_1 = list(range(19, 40))
row_2 = list(range(40, 63))
row_3 = list(range(63, 86))
row_4 = list(range(86, 107))
row_5 = list(range(107, 126))

# Hardware pixel order
# Every other row is reversed
hw_order = row_0 + list(reversed(row_1)) + row_2 + list(reversed(row_3)) + row_4 + list(reversed(row_5))

# Some color constants
COLOR_BLACK = "#000000"
COLOR_WHITE = "#FFFFFF"
COLOR_ORANGE = "#FFA500"
COLOR_BLUE = "#0000FF"
COLOR_GREEN = "#008000"
