"""Hardware interface to the NeoPixels

Modified from; https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
"""

import characters

try:
    import board
    import neopixel

    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    pixel_pin = board.D18
    num_pixels = 126

    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)

except (ModuleNotFoundError, NotImplementedError):
    num_pixels = 126
    pixels = None


# Hardware pixel order
# Every other row is reversed
pixel_index_map = (
    characters.row_0
    + list(reversed(characters.row_1))
    + characters.row_2
    + list(reversed(characters.row_3))
    + characters.row_4
    + list(reversed(characters.row_5))
)


def hex_to_rgb(chex):
    """Convert color hex string to (r,g,b) tuple.
    """
    chex = chex.lstrip("#")
    return tuple(int(chex[ii : ii + 2], 16) for ii in (0, 2, 4))


def write(color_list):
    """Write a list of css-style hex colors to the clock.

    color_list = ["#000000", "#ffffff", ...]
    """
    if pixels:
        # Write each pixel according to the hardware index
        for ii in range(num_pixels):
            # Remap standard indexing to the alternating
            #   rows that are implemented in hardware.
            index = pixel_index_map[ii]
            color = hex_to_rgb(color_list[ii])
            pixels[index] = color
        # Write to the pixels
        pixels.show()
