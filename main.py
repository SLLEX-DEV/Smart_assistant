from core.wake_word import wakeWord
from core.audio_manager import AudioManager
from core.scripts1 import cv2_to_ai,char_compare
from core.vision import CameraController
from core.voice import Voice_listener
from core.voice_generate import tts
from core.ai_engine import AiEngine
import threading
from multiprocessing import Process,Pipe
from collections import deque

 def cameraManager(pipe):
    cameraC = CameraController()
    while True:
        if pipe.poll(1):
            task = pipe.recv()
            if task == 'ImGemini':
                pipe.send(cameraC.get_frame())

def sttManager(pipe):
    audioDeq =  deque(maxlen=60)
    ww = wakeWord()
    audioM = AudioManager(audioDeq)
    VoiceL = Voice_listener()
    stat = 'waiting'
    audioM.start()

    while True:
        if len(audioDeq) > 0:
            char = audioDeq.popleft()

            match stat:
                case 'waiting':
                    if ww.frazeDetect(char) == 0:
                        stat = "listening"
                case 'listening':
                    fraze = VoiceL.Getfraze(char)
                    if fraze:
                        pipe.send(fraze)
                        stat = "waiting"







def main():
    voskConn1,voskConn2 = Pipe()
    cameraConn1,cameraConn2 = Pipe()

    processSttManager = Process(target = sttManager, args = voskConn2)
    processCameraManager = Process(target = cameraManager, args = cameraConn2)

    processSttManager.start()
    processCameraManager.start()

def mainloop():

    while True:

