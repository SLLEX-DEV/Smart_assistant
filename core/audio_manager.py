import threading
from itertools import cycle
import sounddevice as sd
from collections import deque
import threading as thread




class AudioManager:
    def __init__(self,devise_number,deque):
        self.devise_number = devise_number
        sd.default.device = devise_number
        self.deque = deque
        self.stream = None
    def audioCycle(self,indata,frame,time,status):
        if  status:
            print('audioError')
        chunk = indata.reshape(-1).copy()
        self.deque.append(chunk)
    def cycle(self):
            self.stream = sd.InputStream(
               samplerate=16000,
               blocksize=512,
               device=self.devise_number,
               channels=1,
               dtype='int16',
               latency=0.02,
               callback=self.audioCycle)

            self.stream.start()
    def start(self):
        self.thredAudio = threading.Thread(target=self.cycle,daemon=True)
        self.thredAudio.start()
    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()



