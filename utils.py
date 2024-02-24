import face_recognition
import cv2
import numpy as np
import os, datetime
import json

IMAGE_DB_PATH="./images/"

def get_camera_details () -> tuple :
    with open('config.json') as f:
        data = json.load(f)
    return ((i, data[str(i)]["mode_of_operation"], data[str(i)]["camera_id"], data[str(i)]["class_id"]) for i in range(len(data))) 
