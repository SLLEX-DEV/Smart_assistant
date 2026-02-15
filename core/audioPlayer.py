import sounddevice as sd
import queue
import threading


class audioPlayer():
    def __init__(self,devise_num = None):
        if devise_num is not None:
            sd.default.device = devise_num
    def playLoop(self,queue):
        while True:
                audio = queue.get()
                if audio:
                    sd.play(audio.samples,samplerate=audio.sample_rate)
                    sd.wait()
    def loopStart(self,queue):
        playThread = threading.Thread(target=self.playLoop,args=(queue,),daemon=True)
        playThread.start()

    def errorStop(self):
        sd.stop()

