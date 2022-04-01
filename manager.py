"""Toblerone Clock Model.
"""

import time
import threading
import datetime

import numpy as np

import core
import characters
import animations
import pride
import hardware


def clock():
    dt = datetime.datetime.now()
    return animations.clock_face(dt)


def flags():
    while True:
        for key in pride.flags.keys():
            yield pride.flag(key)


class TobleroneClock(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store color list
        self._color_list = ["#000000"] * characters.num_pixels
        # Store coordinates
        (self._x0, self._y0, self._xs, self._ys) = map(np.array, core.extended())
        # This maps the current state of the clock to;
        #   (
        #       a function that will return a new color list,
        #       the delay between calls to that function
        #   )
        self._animations = {
            "clock": (clock, 0.5),
            "pride": (flags, 10),
            "custom": (self._color_list, 0.5),
        }
        self.set_animation("clock")

    def _get_data(self):
        """Call the animation function and return the color list and delay.
        """
        color_fcn, delay = self._animations[self._current_animation]
        color_list = color_fcn()
        return (color_list, delay)

    @property
    def color_list(self):
        """Return the current face color list.
        """
        color_list, _ = self._get_data()
        return color_list

    def run(self):
        """Main thread method - update the clock forever.
        """
        while True:
            color_list, delay = self._get_data()
            hardware.write(color_list)
            time.sleep(delay)

    def set_animation(self, key):
        """Set the animation to one of the animation keys.
        """
        if key in self._animations.keys():
            self._current_animation = key
        else:
            raise ValueError("Requested animation key not found.")

    def set_pixel(self, index, color):
        """Set a specific pixel to a specific color.
        """
        self._color_list[index] = color

    def set_all(self, color):
        """Set all pixels to a given color.
        """
        for ii in range(characters.num_pixels):
            self.set_pixel(ii, color)
