import sherpa_onnx as sh
import queue


class tts:
    def __init__(self):
            self.model_path=r'assets\models\sherpaVoice\voice.onnx'
            self.tokens_path=r'assets\models\sherpaVoice\tokens.txt'
            self.data_dir_path=r'assets\models\sherpaVoice\espeak-ng-data'
    def initializate(self):
        vits = sh.OfflineTtsVitsModelConfig(
            model=self.model_path,
            lexicon='',
            tokens=self.tokens_path,
            data_dir=self.data_dir_path,
            noise_scale=0.667,
            noise_scale_w=0.9,
            length_scale=1.4
        )
        config = sh.OfflineTtsModelConfig(
            vits=vits,
            num_threads=2,
            debug=False
        )
        tts_config = sh.OfflineTtsConfig(
            model=config
        )

        self.tts = sh.OfflineTts(config=tts_config)
    def generateAudio(self, text,queue):
        audio = self.tts.generate(text)
        queue.put(audio)