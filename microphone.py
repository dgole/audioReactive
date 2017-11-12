# sets up an audio stream from the microphone
import time
import numpy as np
import pyaudio
import config


class Stream():
    def __init__(self):
        print('initiating stream object')
        self.frameCount = 0
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
    def readNewData(self):
        try:
            self.micData = np.fromstring(self.stream.read(self.frames_per_buffer), dtype=np.int16)
            self.micData = self.micData.astype(np.float32)
            print('successfully got data from audio stream')
            self.frameCount += 1
        except IOError:
            print('failed to get data from audio stream')
            self.overflows += 1        
    def stopStream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    def getSpectrum(self):
        # Transform audio input into the frequency domain
        n = len(self.micData)
        # Pad with zeros until the next power of two
        nZeros = 2**int(np.ceil(np.log2(n))) - n
        nTot = n + nZeros
        micData_padded = np.pad(self.micData, (0, nZeros), mode='constant')
        freqs = np.fft.fftfreq(nTot, d=1./config.MIC_RATE)
        spectrum = np.abs(np.fft.rfft(micData_padded)[:nTot // 2])
        return freqs[0:nTot//2], spectrum[0:nTot//2]

    
        
