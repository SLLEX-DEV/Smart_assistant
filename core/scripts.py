from PIL import Image
import cv2
import numpy as np
import json

def cv2_to_ai(camera_frame):
    camera_frame = cv2.cvtColor(camera_frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(camera_frame)
def jsonTOdict(json):
    return json.loads(json)
