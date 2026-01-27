import sounddevice as sd
import queue



class AudioManager:
    def __init__(self,devise_number = 1):
        self.devise_number = devise_number
        sd.default.device(devise_number)
        self.frameQueue = queue.Queue()
        self.stream = None
    def audioCycle(self,indata,frame,time,status):
        if  status:
            print('audioError')
        self.frameQueue.put(indata.copy())
    def start(self):
            self.stream = sd.RawInputStream(
               samplerate=16000,
               blocksize=512,
               device=self.devise_number,
               channels=1,
               dtype='int16',
               callback=self.audioCycle)
            self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            print('stream offline')


