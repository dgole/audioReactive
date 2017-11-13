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
def getFreqsToMelMatrix(freqs, dMel=1):
    melMin = np.ceil(hertzToMel(freqs[1]))
    melMax = np.floor(hertzToMel(freqs[-1]))
    nFreqs = len(freqs)
    nMels = (melMax-melMin+1)/dMel
    mels = np.arange(melMin, melMax+1, dMel)
    centerFreqs    = [melToHertz(mel)          for mel in mels]
    lowerEdgeFreqs = [melToHertz(mel-dMel/2.0) for mel in mels]
    upperEdgeFreqs = [melToHertz(mel+dMel/2.0) for mel in mels]
    freqsToMelMatrix = np.zeros([nMels, nFreqs])
    for i in range(nMels):
        for j in range(nFreqs):
            if lowerEdgeFreqs[i] < freqs[j] < upperEdgeFreqs[i]:
                freqsToMelMatrix[i,j] = 1.0 
 


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
        self.nSamples = len(self.micData)
        self.nZeros = 2**int(np.ceil(np.log2(self.nSamples))) - self.nSamples
        self.nSamplesPadded = self.nSamples + self.nZeros
        micData_padded = np.pad(self.micData, (0, nZeros), mode='constant')
        self.freqs = np.fft.fftfreq(self.nSamplesPadded, d=1./config.MIC_RATE)
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
        # Pad with zeros until the next power of two
        micData_padded = np.pad(self.micData, (0, nZeros), mode='constant')
        spectrum = np.abs(np.fft.rfft(micData_padded)[:self.nTot // 2])
        return spectrum[0:nTot//2]
    
    
     
    
    
    
    
    
    
    
    

    
        
