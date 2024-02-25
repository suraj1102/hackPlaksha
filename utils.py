import face_recognition
import cv2
import numpy as np
import os, datetime
import json
import sqlite3
import threading

IMAGE_DB_PATH="./images/"

def get_camera_details () -> tuple :
    with open('config.json') as f:
        data = json.load(f)

    return (
        data["class_id"],
        data["cameras"]
    )