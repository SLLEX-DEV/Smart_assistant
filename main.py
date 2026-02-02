from core.wake_word import wakeWord
from core.audio_manager import AudioManager
from core.scripts1 import cv2_to_ai,jsonTOdict,char_compare
from core.vision import CameraController
from core.voice import Voice_listener
from core.voice_generate import tts
import threading
import  time

#инит
WW = wakeWord()
AM = AudioManager(devise_number=1)
camera = CameraController()
Vl  = Voice_listener()
tts = tts()

# потоки
thread1 = threading.Thread(target=AM.start,daemon=True)
thread1.start()
part = 'waiting'
while True:
    audio = AM.frame_queue.get()
    AM.frame_queue.task_done()
    convertedAudio = audio.flatten()
    match part:
        case 'waiting':
            if WW.frazeDetect(convertedAudio) == 0:
                part = 'listening'
        case 'listening':
            fraze = Vl.Getfraze(convertedAudio.tobytes())
            result_dict = jsonTOdict(fraze)
            text = result_dict.get('text','')
            print('1')
            print(text)
            part = 'waiting'








