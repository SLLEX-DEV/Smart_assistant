from random import sample
import vosk
from vosk import Model, KaldiRecognizer
import  sounddevice as sd
import threading




class Voice_listener:
    def __init__(self,model = r'assets\models\vosk_model',devise_num = 1):
        self.devise_num = devise_num
        self.model = model
        self.modelPath = vosk.Model(model_path=model)
        self.rec = vosk.KaldiRecognizer(self.modelPath,16000)
    def Getfraze(self,sounds):
         if not self.rec.AcceptWaveform(sounds):
            result =self.rec.Result()
            return result



