import os
from os import access
import pvporcupine as prc
from dotenv import load_dotenv


class wakeWorld:
    def __init__(self,keyword):
        load_dotenv()
        self.access_key = os.getenv('wake_word_key')
        self.keyword = [keyword]
        self.wakeWd = prc.create(access_key=self.access_key,keywords=keyword,\
                                model_path='smart_assistant/assets/models/wake_word_model')
    def frazeDetectP(self,message):
        isCalling =  self.wakeWd.process(message)
        self.wakeWd.delete()
        return  isCalling
