# sets up an audio stream from the microphone
import time
import numpy as np
import pyaudio
import config


class Stream():
    def __init__(self):
        print('initiating stream object')
        self.p = pyaudio.PyAudio()
        self.frames_per_buffer = int(config.MIC_RATE / config.FPS)
        self.stream = self.p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=config.MIC_RATE,
                        input=True,
                        frames_per_buffer=self.frames_per_buffer)
        self.overflows = 0
        self.prev_ovf_time = time.time()
        print('stream object initiated')
    def getData(self):
        try:
            y = np.fromstring(self.stream.read(self.frames_per_buffer), dtype=np.int16)
            y = y.astype(np.float32)
            print('successfully got data from audio stream')
            return(y)
        except IOError:
            print('failed to get data from audio stream')
            self.overflows += 1        
    def stopStream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    
def calcSpectrum(micData):
    # Transform audio input into the frequency domain
    N = len(micData)
    # Pad with zeros until the next power of two
    N_zeros = 2**int(np.ceil(np.log2(N))) - N
    #micData *= fft_window
    micData_padded = np.pad(micData, (0, N_zeros), mode='constant')
    spectrum = np.abs(np.fft.rfft(micData_padded)[:N // 2])
    return spectrum
    
        
