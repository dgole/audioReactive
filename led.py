from __future__ import print_function
from __future__ import division

import platform
import numpy as np
import config
import neopixel


# create strip object with parameters from config file
strip = neopixel.Adafruit_NeoPixel(config.nLed, 
                                   config.LED_PIN,
                                   config.LED_FREQ_HZ,
                                   config.LED_DMA,
                                   config.LED_INVERT,
                                   config.BRIGHTNESS)
# initialize strip
strip.begin()
prev_pixels = np.tile(253, (3, local_N_PIXELS))
pixels = np.tile(1, (3, local_N_PIXELS))

def update():
    global pixels, prevPixels
    # Truncate values and cast to integer
    pixels = np.clip(pixels, 0, 255).astype(int)
    # Encode 24-bit LED values in 32 bit integers
    r = np.left_shift(p[0][:].astype(int), 8)
    g = np.left_shift(p[1][:].astype(int), 16)
    b = p[2][:].astype(int)
    rgb = np.bitwise_or(np.bitwise_or(r, g), b)
    # Update the pixels
    for i in range(local_N_PIXELS):
        # Ignore pixels if they haven't changed (saves bandwidth)
        if np.array_equal(p[:, i], _prev_pixels[:, i]):
            continue
        strip._led_data[i] = rgb[i]
    _prev_pixels = np.copy(p)
    strip.show()
