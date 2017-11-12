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
            y = np.fromstring(stream.read(frames_per_buffer), dtype=np.int16)
            y = y.astype(np.float32)
            return(y)
        except IOError:
            self.overflows += 1        
    def stopStream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
