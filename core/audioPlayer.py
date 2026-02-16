import sounddevice as sd
import queue
import threading
import numpy as np


class audioPlayer():
    def __init__(self,devise_num = None):
        if devise_num is not None:
            sd.default.device = devise_num
    def playLoop(self,queue):
        while True:
                audio = queue.get()
                if audio:
                    try:
                        stereo_samples = np.column_stack((audio.samples, audio.samples))
                        sd.play(stereo_samples,samplerate=audio.sample_rate)
                        sd.wait()
                    except Exception as e:
                        print(e)
    def loopStart(self,queue):
        playThread = threading.Thread(target=self.playLoop,args=(queue,),daemon=True)
        playThread.start()

    def errorStop(self):
        sd.stop()

