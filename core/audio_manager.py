import sounddevice as sd
import queue





class AudioManager:
    def __init__(self,devise_number):
        self.devise_number = devise_number
        sd.default.device = devise_number
        self.stream = None
        self.frame_queue = queue.Queue()
    def audioCycle(self,indata,frame,time,status):
        if  status:
            print('audioError')
        self.frame_queue.put(indata.reshape(-1).copy())
    def start(self):
            self.stream = sd.InputStream(
               samplerate=16000,
               blocksize=512,
               device=self.devise_number,
               channels=1,
               dtype='int16',
               latency=0.02,
               callback=self.audioCycle)

            self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            print('stream offline')


