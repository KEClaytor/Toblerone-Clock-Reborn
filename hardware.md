# Hardware Notes

## Which pixels

Neopixels vs. dotstars?

What sort of spacing do we need (2 measurements on the toblerone spacing):
- 40 mm / 2 pixels = 20 mm / px
- 115 mm / 6 pixels = 19.16 mm / px

Spacing for a 30 px / m
- 1000 mm / 30 px = 33 mm / px - a little too much

[Best price on flexible connected pixels](https://www.adafruit.com/product/4560)
These look like the best, as I can center each one on the tube.

## Estimating power draw

[Powering guide](https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels)

126 NeoPixels × 20 mA ÷ 1,000 = 2.52 Amps minimum
126 NeoPixels × 60 mA ÷ 1,000 = 7.56 Amps maximum

## External displays

[Display for Pi v1](https://www.adafruit.com/product/2097)
[Display for Pi 2+/0](https://www.adafruit.com/product/2441)

Do I even need a display?
I can just run the bokeh server over the local LAN and use an existing computer.

Do I want a display...?

## Wiring neopixels

[Pi <--> Neopixel wiring guide](https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring)
Looks like I'll need either a [level shifter](https://www.adafruit.com/product/1787) (preferred) or a diode (see below).

> GPIO18 is the standard pin

> The diodes Adafruit sells only handle 1 Amp of continuous current so they're good for driving up to about 16 NeoPixels at full 100% bright white - and about 50 NeoPixels if they're all lit with various colors
