import sherpa_onnx as sh


class TTS:
    def __init__(self):
        vits = sh.OfflineTtsVitsModelConfig(
            model=r'smart_assistant\assets\models\sherpaVoice\voice.onnx',
            lexicon='',
            tokens=r'smart_assistant\assets\models\sherpaVoice\tokens.txt',
            data_dir=r'smart_assistant\assets\models\sherpaVoice\espeak-ng-data',
            noise_scale=0.667,
            noise_scale_w=0.9,
            length_scale=1.2
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
    def generateAudio(self, text):
        self.audio = self.tts.generate(text)

