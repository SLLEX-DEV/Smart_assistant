import cv2
import threading
import time



class CameraController:
    def __init__(self, camera_number=0):
        self.camera_number = camera_number

    def start(self):
        self.cap = cv2.VideoCapture(self.camera_number)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.ret, self.frame = False, None
        self.stopped = False
#==СОЗДАНИЕ ОТДЕЛЬНОГО ПОТОКА ДЛЯ КАМЕРЫ==
        t = threading.Thread(target=self._update, args=(), daemon=True)
        t.start()
        time.sleep(1.0)
        return self
#==ЦИКЛ ЗАПОЛНЕНИЯ БУФЕРА КАДРАМИ==
    def _update(self):
        while not self.stopped:
            if not self.cap.isOpened():
                self.stopped = True
                break
            self.ret, self.frame = self.cap.read()

            if not self.ret:
                self.stopped = True
#==БЕРЕМ ОДИН КАДР ИЗ БУФЕРА==
    def get_frame(self):
         if self.frame is None:
             return None
         frameC = self.frame.copy()
         stat,Convframe = cv2.imencode('.jpg',frameC,[int(cv2.IMWRITE_JPEG_QUALITY),90])
         if stat:
            return Convframe.tobytes()
         return None

    def stop(self):
        self.stopped = True
        self.cap.release()




