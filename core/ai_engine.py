
from google import genai
import os
from dotenv import load_dotenv
from google.genai import  types


class AiEngine():


    def __init__(self,model_name = 'gemini-2.5-flash-lite'):
        self.model_name = model_name
        load_dotenv()
        self.api_key = os.getenv('gemini_api_key')
        if not self.api_key:
            raise ValueError("need api key!!!")
        self.client = genai.Client(api_key=self.api_key)
    def image_info(self,promt,image):
        response = self.client.models.generate_content(
            model= self.model_name,
            contents=[image,promt],
            config = types.GenerateContentConfig(
            system_instruction="ты помошник для незрячих;  отвечай быстро и кратко;не давай сильно\
             красочных описаний;главное безоапасность",
            temperature = 0.3
            )
        )
        return response.text









