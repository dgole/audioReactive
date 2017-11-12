from __future__ import print_function
from __future__ import division

import platform
import numpy as np
import time
import config
import neopixel
import microphone

# create strip object with parameters from config file
strip = neopixel.Adafruit_NeoPixel(config.nLed, 
                                   config.LED_PIN,
                                   config.LED_FREQ_HZ,
                                   config.LED_DMA,
                                   config.LED_INVERT,
                                   config.BRIGHTNESS)
# initialize strip
strip.begin()
prevPixels = np.tile(253, (3, config.nLed))
pixels = np.tile(0, (3, config.nLed))
print(prevPixels.shape)
print(pixels.shape)

def update():
    global pixels, prevPixels
    # Truncate values and cast to integer
    pixels = np.clip(pixels, 0, 255).astype(int)
    p = np.copy(pixels)
    # Encode 24-bit LED values in 32 bit integers
    r = np.left_shift(p[0][:].astype(int), 8)
    g = np.left_shift(p[1][:].astype(int), 16)
    b = p[2][:].astype(int)
    rgb = np.bitwise_or(np.bitwise_or(r, g), b)
    # Update the pixels
    for i in range(config.nLed):
        # Ignore pixels if they haven't changed (saves bandwidth)
        if np.array_equal(p[:, i], prevPixels[:, i]):
            continue
        strip._led_data[i] = rgb[i]
    strip.show()

stream = microphone.Stream()
while True:
    micData = stream.getData()
    if micData is not None:
        spectrum = microphone.calcSpectrum(micData)
        pixels[0,:] = spectrum[10] / 1.e4
        update()
    



