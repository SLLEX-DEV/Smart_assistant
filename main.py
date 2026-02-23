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
# ==ОБРАБОТКА И ОТПРАВКА SHERPA+AUDIOPLAYER==
def ttsManager(pipe):
    sherpa = tts()
    audioPlay = audioPlayer(3)

    sherpa.initializate()
#==ОЧЕРЕДЬ ДЛЯ АУДИО==
    audioQueue = queue.Queue()

    audioPlay.loopStart(audioQueue)
    while True:
        if pipe.poll(0.1):
            fraze = pipe.recv()
            if fraze == 'stop':
                audioPlay.errorStop()

            sherpa.generateAudio(fraze,audioQueue)
#==БЕРЕТ КАДР ИЗ БУФЕРА ПРИ ЗАПРОСЕ==
def cameraManager(pipe):
    cameraC = CameraController()
    cameraC.start()
    while True:
        if pipe.poll(1):
            task = pipe.recv()
            if task == 'stop':
                cameraC.stop()
            elif task == 'ImGemini':
                try:
                    pipe.send(cameraC.get_frame())
                except Exception as e:
                    print(e)
#==ОБРАБОТЧИК WW И ПРЕОБРАЗОВАТЕЛЬ  STT==
def sttManager(pipe):
    audioDeq =  deque(maxlen=60)
    ww = wakeWord()
    audioM = AudioManager(1 ,audioDeq)
    VoiceL = Voice_listener()
    VoiceL.initialization()
    stat = 'waiting'


    audioM.start()

    while True:
        if pipe.poll(0.1):
            if pipe.recv == 'stop':
                audioM.stop()
        if len(audioDeq) > 0:
            char = audioDeq.popleft()

            match stat:
                case 'waiting':
                    if ww.frazeDetect(char) == 0:
                        print('1')
                        stat = "listening"
                case "listening":
                    fraze = VoiceL.Getfraze(char.tobytes())
                    if fraze:
                        pipe.send(fraze)
                        stat = "waiting"







def main():
#==СОЗДАНИЕ ТРУБ ДЛЯ ПРОЦЕССОВ==
    voskConn1,voskConn2 = Pipe()
    cameraConn1,cameraConn2 = Pipe()
    SGconn1,SGconn2 = Pipe()
#==ИНИЦИАЛИЗАЦИЯ ПРОЦЕССОВ==
    processSttManager = Process(target = sttManager, args = (voskConn2,))
    processCameraManager = Process(target = cameraManager, args = (cameraConn2,))
    processGemini2Sherpa = Process(target=ttsManager,args=(SGconn2,))

    processSttManager.start()
    processCameraManager.start()
    processGemini2Sherpa.start()
#==ЗАПУСК ГЛАВНОГО ЦИКЛА В asyncio==
    try:
        asyncio.run(mainloop(cameraConn1, voskConn1, SGconn1))
    except Exception as e:
        print(e)

#==ГЛАВНЫЙ ЦИКЛ ОБРАБОТКИ ДАННЫХ==
async def mainloop(cameraPipe,voskPipe,audioPipe):
    gem = AiEngine()
    wordC = Wordcompair()
    task = ''
    while True:
        if voskPipe.poll(0.1):
#==ОПРЕДЕЛЕНИЕ КАТЕГОРИИ ЗАПРОСА==
            text = voskPipe.recv()
            promt,task = wordC.wordAnalize(text)
            print(task)
            print(promt)
            match task:
                case 'local':
                    if promt == 'stop':
                        print('stop')
                    audioPipe.send(promt)
                case 'gemini':
                    print('2')
                    res = gem.image_info(promt)
                    async for chank in res:
                        audioPipe.send(chank)
                case 'ImGemini':
                    cameraPipe.send('ImGemini')
                    if cameraPipe.poll(0.1):
                        image = cameraPipe.recv()

                        res = gem.image_info(promt,image)
                        async for chank in res:
                            print(chank)
                            audioPipe.send(chank)
                case _:
                    break
if __name__ == '__main__':
    main()





