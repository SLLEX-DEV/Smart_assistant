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
                        samples = audio.samples
                        sr = audio.sample_rate
                        silence_duration = 0.1
                        silence = np.zeros(int(sr * silence_duration), dtype=np.float32)
                        padded_audio = np.concatenate([samples, silence])
                        sd.play(padded_audio,samplerate=sr)
                        sd.wait()
                    except Exception as e:
                        print(e)
    def loopStart(self,queue):
        playThread = threading.Thread(target=self.playLoop,args=(queue,),daemon=True)
        playThread.start()

    def errorStop(self):
        sd.stop()

