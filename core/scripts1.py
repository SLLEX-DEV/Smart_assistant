from PIL import Image
import cv2
import numpy as np
import json
from rapidfuzz import process,fuzz,utils


def cv2_to_ai(camera_frame):
    camera_frame = cv2.cvtColor(camera_frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(camera_frame)
def char_compare(user_input,commands):
    result = process.extractOne(
        user_input,
        commands,
        scorer=fuzz.WRatio,
        processor=utils.default_process,
        score_cutoff=80)
    if result:
        return result[0]
    return user_input
