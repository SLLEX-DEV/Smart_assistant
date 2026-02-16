import asyncio

from core.wake_word import wakeWord
from core.audio_manager import AudioManager
from core.vision import CameraController
from core.voice import Voice_listener
from core.voice_generate import tts
from core.ai_engine import AiEngine
from core.audioPlayer import audioPlayer
from multiprocessing import Process,Pipe
from collections import deque
from core.rapidFuzz import Wordcompair
import queue
def ttsManager(pipe):
    sherpa = tts()
    audioPlay = audioPlayer()

    sherpa.initializate()
    audioQueue = queue.Queue()

    audioPlay.loopStart(audioQueue)
    while True:
        if pipe.poll(None):
            fraze = pipe.recv()
            sherpa.generateAudio(fraze,audioQueue)
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
    audioM = AudioManager(1,audioDeq)
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
    SGconn1,SGconn2 = Pipe()

    processSttManager = Process(target = sttManager, args = (voskConn2,))
    processCameraManager = Process(target = cameraManager, args = (cameraConn2,))
    processGemini2Sherpa = Process(target=ttsManager,args=(SGconn2,))

    processSttManager.start()
    processCameraManager.start()
    processGemini2Sherpa.start()
    asyncio.run(mainloop(cameraConn1,voskConn1,SGconn1))

async def mainloop(cameraPipe,voskPipe,audioPipe):
    gem = AiEngine()
    wordC = Wordcompair()
    task = ''
    while True:
        if voskPipe.poll(None):
            text = voskPipe.recv()
            promt,task = wordC.wordAnalize(text)
            match task:
                case 'local':
                    print(promt)
                case 'gemini':
                    res = gem.image_info(promt)
                    for chank in res:
                        audioPipe.send(chank)
                case 'ImGemini':
                    cameraPipe.send('ImGemini')
                    if cameraPipe.poll(None):
                        image = cameraPipe.recv()
                        res = gem.image_info(promt,image)
                        for chank in res:
                            audioPipe.send(chank)
if __name__ == '__main__':
    main()





