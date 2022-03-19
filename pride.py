"""Patterns for Pride (LGBTQ+) flags for the extended layout.


Flag colors from:
    General
        https://www.schemecolor.com/lgbt-flag-colors.php
    Sexual Orientation
        https://www.schemecolor.com/new-lesbian-flag-colors.php
        https://www.schemecolor.com/bisexuality-flag-colors.php
        https://www.schemecolor.com/pansexuality-flag-colors.php
        https://www.schemecolor.com/asexual-pride-flag-colors.php
        https://www.schemecolor.com/demisexual-flag-colors.php
    Gender Identity
        https://www.schemecolor.com/cisgender-flag-colors.php
        https://www.schemecolor.com/transgender-pride-flag-colors.php
        https://www.schemecolor.com/non-binary-gender-flag-colors.php
        https://www.schemecolor.com/polygender-flag-colors.php
        https://www.schemecolor.com/genderfluidity-pride-flag-colors.php
        https://www.schemecolor.com/agender-pride-flag-colors.php
    Intersex
        https://www.schemecolor.com/intersex-flag-colors.php
    Aro/Ace
        https://www.schemecolor.com/aromantic-flag-colors.php
"""

import numpy as np

import core

import core
import characters

# Convience dictionary that maps colors to rows/chevrons
flags = {
    # flag_name: [(color, pattern), ...]
    # General
    "rainbow": [
        ("#FF0018", "row0"),
        ("#FFA52C", "row1"),
        ("#FFFF41", "row2"),
        ("#008018", "row3"),
        ("#0000F9", "row4"),
        ("#86007D", "row5"),
    ],
    "progress": [
        ("#FF0018", "row0"),
        ("#FFA52C", "row1"),
        ("#FFFF41", "row2"),
        ("#008018", "row3"),
        ("#0000F9", "row4"),
        ("#86007D", "row5"), 
        ("#FFFFFF", "chevron0"),
        ("#F7A8B8", "chevron1"),
        ("#55CDFC", "chevron2"),
        ("#63531F", "chevron3"),
        ("#000000", "chevron4"),
    ],
    # Sexual Orientation
    "lesbian": [
        ("#D62900", "row0"), # Extra
        ("#D62900", "row1"),
        ("#FF9B55", "row2"),
        ("#FFFFFF", "row3"),
        ("#D461A6", "row4"),
        ("#A50062", "row5"),
    ],
    "bisexual": [
        ("#D60270", "row0"),
        ("#D60270", "row1"),
        ("#9B4F96", "row2"),
        ("#9B4F96", "row3"),
        ("#0038A8", "row4"),
        ("#0038A8", "row5"),
    ],
    "pansexual": [
        ("#FF1B8D", "row0"),
        ("#FF1B8D", "row1"),
        ("#FFDA00", "row2"),
        ("#FFDA00", "row3"),
        ("#1BB3FF", "row4"),
        ("#1BB3FF", "row5"),
    ],
    "asexual": [
        ("#000000", "row0"), # Extra
        ("#000000", "row1"),
        ("#A4A4A4", "row2"),
        ("#FFFFFF", "row3"),
        ("#810081", "row4"),
        ("#810081", "row5"), # Extra
    ],
    "demisexual": [
        ("#FFFFFF", "row0"),
        ("#FFFFFF", "row1"),
        ("#810081", "row2"), # Extra
        ("#810081", "row3"),
        ("#A4A4A4", "row4"),
        ("#A4A4A4", "row5"),
        ("#000000", "chevron0"),
        ("#000000", "chevron1"),
        ("#000000", "chevron2"),
        ("#000000", "chevron3"),
        ("#000000", "chevron4"),
    ],
    # Gender Identity
    "cisgender": [
        ("#D75495", "row0"),
        ("#D75495", "row1"),
        ("#D75495", "row2"),
        ("#001FA7", "row3"),
        ("#001FA7", "row4"),
        ("#001FA7", "row5"),
    ],
    "transgender": [
        ("#55CDFC", "row0"),
        ("#F7A8B8", "row1"),
        ("#FFFFFF", "row2"), # Extra
        ("#FFFFFF", "row3"),
        ("#F7A8B8", "row4"),
        ("#55CDFC", "row5"),
    ],
    "nonbinary": [
        ("#FFF430", "row0"), # Extra
        ("#FFF430", "row1"),
        ("#FFFFFF", "row2"),
        ("#9C59D1", "row3"),
        ("#000000", "row4"),
        ("#000000", "row5"), # Extra
    ],
    "polygender": [
        ("#000000", "row0"), # Extra
        ("#939393", "row1"),
        ("#EC95C5", "row2"),
        ("#F5ED80", "row3"),
        ("#65BBE7", "row4"),
        ("#000000", "row5"),
    ],
    "genderfluid": [
        ("#000000", "row0"), # Extra
        ("#FF76A4", "row1"),
        ("#FFFFFF", "row2"),
        ("#C011D7", "row3"),
        ("#000000", "row4"),
        ("#2F3CBE", "row5"),
    ],
    "agender": [
        ("#000000", "row0"),
        ("#BABABA", "row1"),
        # ("#FFFFFF", "row2"), # Missing
        ("#BAF584", "row2"),
        ("#FFFFFF", "row3"),
        ("#BABABA", "row4"),
        ("#000000", "row5"),
    ],
    # Sex
    "intersex": [
        ("#FFDA00", "row0"),
        ("#FFDA00", "row1"),
        ("#FFDA00", "row2"),
        ("#7A00AC", "row3"),
        ("#7A00AC", "row4"),
        ("#7A00AC", "row5"), # Extra
    ],
    # Other
    "aromantic": [
        ("#3AA63F", "row0"),
        ("#A8D47A", "row1"),
        ("#FFFFFF", "row2"),
        ("#AAAAAA", "row3"),
        ("#000000", "row4"),
        ("#000000", "row5"), # Extra
    ],
}

# Core patterns
patterns = {
    # name: (character, shift)
    "row0": (characters.row_0, 0),
    "row1": (characters.row_1, 0),
    "row2": (characters.row_2, 0),
    "row3": (characters.row_3, 0),
    "row4": (characters.row_4, 0),
    "row5": (characters.row_5, 0),
    "chevron0": (characters.chevron_right, -6),
    "chevron1": (characters.chevron_right, -4),
    "chevron2": (characters.chevron_right, -2),
    "chevron3": (characters.chevron_right, 0),
    "chevron4": (characters.chevron_right, 2),
}


def flag(flag_name):
    """Create a pride flag for display.
    """
    colors = np.array(["#000000"] * 126, dtype=object)
    for color, p in flags[flag_name]:
        (index, shift) = patterns[p]
        colors[core.shift(index, shift)] = color

    return colors
