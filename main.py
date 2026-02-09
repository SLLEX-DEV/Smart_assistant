from core.wake_word import wakeWord
from core.audio_manager import AudioManager
from core.scripts1 import cv2_to_ai,char_compare
from core.vision import CameraController
from core.voice import Voice_listener
from core.voice_generate import tts
from core.ai_engine import AiEngine
import threading
import  time
import multiprocessing as mp
import sounddevice as sd
#инит
WW = wakeWord()
AM = AudioManager(devise_number=1)
camera = CameraController()
Vl  = Voice_listener()
tts = tts()
AI =AiEngine()

# потоки
thread1 = threading.Thread(target=AM.start,daemon=True)
thread1.start()
part = 'waiting'
while True:
    audio = AM.frame_queue.get()
    AM.frame_queue.task_done()
    match part:
        case 'waiting':
            #start_time = time.perf_counter()
            detection = WW.frazeDetect(audio)
            #end_time = time.perf_counter()
            #print(f"Porcupine process time: {(end_time - start_time)*1000:.2f} ms")
            if detection == 0:
                    print('hear')
                    part = 'listening'
        case 'listening':
                text = Vl.Getfraze(audio.tobytes())
                if text:
                    part = 'generation'
        case 'generation':
            answer = AI.info(text)
            if answer:
                print(answer)
                part = 'voiceGen'
        case 'voiceGen':
           tts.generateAudio(answer)












