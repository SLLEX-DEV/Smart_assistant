from core.wake_word import wakeWord
from core.audio_manager import AudioManager
from core.scripts1 import cv2_to_ai,char_compare
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
    match part:
        case 'waiting':
                if WW.frazeDetect(audio) == 0:
                    print('hear')
                    part = 'listening'
        case 'listening':
                text = Vl.Getfraze(audio.tobytes())
                if text:
                    print(text)
                    part = ''










