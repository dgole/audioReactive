from __future__ import print_function
from __future__ import division
import os

MIC_RATE = 44100 #Sampling frequency of the microphone in Hz

# 130.81 is c3
MIN_FREQUENCY = 130.81 * 1.0

# 4066.84 is b7 and a half
# 3951.066 is b7
#MAX_FREQUENCY = 3951.066 * 1.0
MAX_FREQUENCY = 9397.27 * 1.0

N_FFT_BINS = 75

N_ROLLING_HISTORY = 2 #Number of past audio frames to include in the rolling window
