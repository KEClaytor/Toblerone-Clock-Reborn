"""Hardware interface to the NeoPixels

Modified from; https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
"""

try:
    import board
    import neopixel

    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    pixel_pin = board.D18
    num_pixels = 125

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    ORDER = neopixel.RGB

    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER
    )


    def hex_to_rgb(str):
        """Convert hex string to (r,g,b) tuple.
        """
        return tuple(int(str[ii:ii+2], 16) for ii in (0, 2, 4))

except ModuleNotFoundError:
    pixels = None
