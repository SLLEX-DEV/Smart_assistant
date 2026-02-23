from rapidfuzz import process, fuzz
import scripts1

class Wordcompair():
    def __init__(self):

        self.module = scripts1
#==КОМАНДЫ ДЛЯ ЗРЕНИЯ==
        self.vision_cmd = [
            'опиши',
            "посмотри",
            'изображение',
            ' описание',
        ]
#== СТАНДАРТНЫЕ КОМАНДЫ БЕЗ gemini==
        self.std_cmd = {
            'сколько времени': 'get_time',
            'какое число': 'get_data',
            'какой сегодня день недели': 'get_day'
        }
#==АЛГОРИТМ ОПРЕДЕЛЕНИЯ ТИПА ЗАПРОСА==
    def wordAnalize(self,text):
        words = text.lower().split()
        if not words :
            return None

        vision_match = process.extractOne(
            ' '.join(words[:2]),
            self.vision_cmd,
            scorer=fuzz.WRatio,
            score_cutoff=85
        )
        if vision_match:
            return text,'ImGemini'
        else:
            command_match = process.extractOne(
                text,
                self.std_cmd.keys(),
                scorer=fuzz.WRatio,
                score_cutoff=75
            )
            if command_match:
                cmd = self.std_cmd[command_match[0]].strip()
                func = getattr(self.module,cmd,None)
                return func(),'local'
            else:
                return text, 'gemini'

