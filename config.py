from __future__ import print_function
from __future__ import division
import os

# LED params
nLed = 60
LED_FREQ_HZ = 800000
LED_PIN = 12
LED_DMA = 5
BRIGHTNESS = 255
LED_INVERT = 0

# Audio params
MIC_RATE = 44100 #Sampling frequency of the microphone in Hz
MIN_FREQUENCY = 130.81 # 130.81 is c3 
MAX_FREQUENCY = 3951.066 # 3951.066 is b7
N_FFT_BINS = 60
N_ROLLING_HISTORY = 2 #Number of past audio frames to include in the rolling window
FPS = 30
