from __future__ import print_function
from __future__ import division
import time
import sys
import numpy as np
from numpy import *
from scipy.ndimage.filters import gaussian_filter1d
import config
import microphone
import led

def visualize_spectrum(y):
    output2 = np.zeros([3, config.nPixels])
    return output2 

fft_window = np.hamming(int(config.MIC_RATE / config.FPS) * config.N_ROLLING_HISTORY)

def microphone_update(audio_samples):
    global y_roll, prev_rms, prev_exp, prev_fps_update, keyGuess, keyStringList
    # Normalize samples between 0 and 1
    y = audio_samples / 2.0**15
    # Construct a rolling window of audio samples
    y_roll[:-1] = y_roll[1:]
    y_roll[-1, :] = np.copy(y)
    y_data = np.concatenate(y_roll, axis=0).astype(np.float32)
    vol = np.max(np.abs(y_data))
    # Transform audio input into the frequency domain
    N = len(y_data)
    #N_zeros = 2**int(np.ceil(np.log2(N))) - N
    # Pad with zeros until the next power of two
    y_data *= fft_window
    #y_padded = np.pad(y_data, (0, N_zeros), mode='constant')
 	#YS = np.abs(np.fft.rfft(y_padded)[:N // 2])
  	YS = np.abs(np.fft.rfft(y_data)[:N // 2])
   	XS = np.fft.rfftfreq(N, d = 1.0 / (config.MIC_RATE))
    # Construct a Mel filterbank from the FFT data
    # Scale data to values more suitable for visualization
    mel = np.dot(mel_y, YS)
    mel = mel**2.0
    # Gain normalization
    mel_gain.update(np.max(gaussian_filter1d(mel, sigma=1.0)))
    mel /= mel_gain.value
    # Map filterbank output onto LED strip
    output = visualization_effect(mel)
    led.pixels = output
    led.update()
   
# Number of audio samples to read every time frame
samples_per_frame = int(config.MIC_RATE / config.FPS)

# Array containing the rolling audio sample window
y_roll = np.random.rand(config.N_ROLLING_HISTORY, samples_per_frame) / 1e16

if __name__ == '__main__':
    # Initialize LEDs
    led.update()
    # Start listening to live audio stream
    microphone.start_stream(microphone_update)
