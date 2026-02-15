from rapidfuzz import process,utils,fuzz


class Wordcompair():
    def __init__(self):
        self.vision_cmd = [
            'опиши',
            "глянь",
            'изображение',
            'дай описание',
            'как выглядит'
        ]
        self.std_cmd = {
            'сколько времени': 'get_time',
            'какое число': 'get_data',
            'какой сегодня день недели': 'get_day'
        }
    def wordAnalize(self,text):
        words = text.lower().split()
        if not words :
            return None

        vision_match = process.extractOne(
            ' '.join(words[:2]),
            self.vision_cmd,
            scorer=fuzz.WRatio,
            score_cutoff=80
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
                return self.std_cmd[command_match[0]],'local'
            else:
                return text, 'gemini'

