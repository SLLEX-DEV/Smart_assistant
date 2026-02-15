import sounddevice as sd


class audioPlayer():
    def __init__(self,devise_num = None):
        if devise_num is not None:
            sd.default.device = devise_num
    def audioPlay(self,audio):
        if audio:
            sd.play(self.audio.samples,samplerate=self.audio.sample_rate)
            sd.wait()
    def errorStop(self):
        sd.stop()

