from vosk import KaldiRecognizer,Model
import json



def json_todict(st):
    return json.loads(st)




class Voice_listener:
    def __init__(self,model = r'assets\models\vosk_model',devise_num = 1):
        self.devise_num = devise_num
        self.model = model
        self.modelPath = Model(model_path=model)
        self.rec = KaldiRecognizer(self.modelPath,16000)
    def Getfraze(self,sounds):
         if self.rec.AcceptWaveform(sounds):
            result =self.rec.Result()
            jsRES = json_todict(result)
            text = jsRES.get('text','')
            return text



