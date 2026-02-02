import os
from os import access
import pvporcupine as prc
from dotenv import load_dotenv



class wakeWord:
    def __init__(self):
        load_dotenv()
        self.access_key = os.getenv('wake_word_key')
        self.wakeWd = prc.create(access_key=self.access_key,keyword_paths=[r'assets\models\wake_word_model\model.ppn'])
    def frazeDetect(self,message):
        isCalling =  self.wakeWd.process(message)
        return  isCalling
