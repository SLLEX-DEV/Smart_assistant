from vosk import Model, KaldiRecognizer
import  sounddevice as sd
import threading



class Voice_listener:
    def __init__(self,model = 'smart_assistant\assets\models\vosk_model',devise_num = 1):
        self.devise_num = devise_num
        self.model = model
        return self
    def start_audio(self):
        rec = Model(self.model)

