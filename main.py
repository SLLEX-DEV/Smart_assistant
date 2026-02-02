from core.wake_word import wakeWord
from core.audio_manager import AudioManager
from core.scripts1 import cv2_to_ai,jsonTOdict,char_compare
from core.vision import CameraController
from core.voice import Voice_listener
from core.voice_generate import tts
import threading


wk = wakeWord()
au = AudioManager(devise_number=1)
thread1 = threading.Thread(target=au.start,daemon=True)
thread1.start()

while True:
    abi = au.frame_queue.get()
    abi2 =abi.flatten()
    print(wk.frazeDetect(abi2))







