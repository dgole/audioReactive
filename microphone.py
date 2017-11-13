# sets up an audio stream from the microphone
import time
import numpy as np
import pyaudio
import config

#####################################
# convert frequencies to notes
#####################################
def hertzToMel(freq):
    return 12.0*(np.log(0.0323963*freq)/0.693147)+12.0
def melToHertz(mel):
    return 440.0 * (2.0**(1.0/12.0))**(mel-58.0)
def getFreqsToMelMatrix(freqMin, freqMax, nFreqs, dMel=1):
    melMin = np.ceil(hertzToMel(freqMin))
    melMax = np.floor(hertzToMel(freqMax))
    nNotes = (melMax-melMin+1)/dMel
    centerFreqs = np.arange(melMin,melMax+dMel,dMel)
    print(centerFreqs.shape)
    print(nNotes)
    freqsToMelMatrix = np.zeros([nFreqs, nNotes])
    #for i in range(nNotes):
        #frequencies_mel = mel_min + delta_mel * arange(-1, num_bands + 1) 
    
#####################################
# Stream class
#####################################
class Stream():
    def __init__(self, nBuffers=4):
        print('initiating stream object')
        self.frameCount = 0
        self.nBuffers = nBuffers
        self.p = pyaudio.PyAudio()
        self.framesPerBuffer = int(config.MIC_RATE / config.FPS)
        self.stream = self.p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=config.MIC_RATE,
                        input=True,
                        frames_per_buffer=self.framesPerBuffer)
        self.overflows = 0
        self.micData = np.zeros(self.framesPerBuffer*self.nBuffers, dtype=np.float32)
        print('stream object initiated')
    def readNewData(self):
        try:
            self.newMicData = np.fromstring(self.stream.read(self.framesPerBuffer), dtype=np.int16)
            self.newMicData = self.newMicData.astype(np.float32)
            self.micData = np.roll(self.micData, -self.framesPerBuffer)
            self.micData[(self.nBuffers-1)*self.framesPerBuffer:(self.nBuffers)*self.framesPerBuffer] = self.newMicData
            print('successfully got data from audio stream')
            self.frameCount += 1
            return True
        except IOError:
            print('failed to get data from audio stream')
            self.overflows += 1
            return False
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
    
    
     
    
    
    
    
    
    
    
    

    
        
