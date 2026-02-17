
from google import genai
import os
from dotenv import load_dotenv
from google.genai import  types


class AiEngine():


    def __init__(self,model_name = 'gemini-2.0-flash-lite'):

        self.model_name = model_name
        load_dotenv()
        self.api_key = os.getenv('gemini_api_key')
        if not self.api_key:
            raise ValueError("need api key!!!")
        self.client = genai.Client(api_key=self.api_key)
    def image_info(self,promt,image = None):
        stopSignal = ('.', '!', '?', '\n')
        buffer = ''
        content = []
        content.append(promt)
        if image is not None:
            image_byt = types.Part.from_bytes(data=image,mime_type='image/jpeg')
            content.append(image_byt)
        response = self.client.models.generate_content_stream(
            model= self.model_name,
            contents = content,
            config = types.GenerateContentConfig(
            system_instruction="ты помошник для незрячих;отвечай не очень обьемно!",
            temperature = 0.3,

            )
        )
        for fraze in response:
            if fraze.text:
                text_part = fraze.text
                buffer += text_part
                if any(p in text_part for p in stopSignal):
                        yield buffer
                        buffer = ''










