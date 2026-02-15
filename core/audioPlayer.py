import sounddevice as sd
import queue


class audioPlayer():
    def __init__(self,devise_num = None):
        if devise_num is not None:
            sd.default.device = devise_num
    def audioPlay(self,audio,queue):
        if queue.qsize() > 0 :
            audio = queue.get()
        if audio:
            sd.play(audio.samples,samplerate=audio.sample_rate)
            sd.wait()
    def errorStop(self):
        sd.stop()

