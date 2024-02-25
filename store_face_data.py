from utils import * 
import face_recognition
import sqlite3
import cv2
import pickle

reference_images = os.listdir(IMAGE_DB_PATH)

db = sqlite3.connect("data.db")

typeOf = int(input("1. Student or 2. TA: "))
name = input("Enter name: ")
id = input("Enter ID: ")

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('Video Feed', frame)

    # Wait for user input
    key = cv2.waitKey(1) & 0xFF

    # If the 's' key is pressed, save the current frame as an image
    if key == ord('s'):
        cv2.imwrite('captured_image.jpg', frame)
        print("Image saved!")
    
    if key == ord('q'):
        break


# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

image = face_recognition.load_image_file("captured_image.jpg")

face_locations = face_recognition.face_locations(image)
face_encodings = face_recognition.face_encodings(image, face_locations)
encoding_dump = pickle.dumps(face_encodings[0])

os.remove("captured_image.jpg")

print(id, name, encoding_dump)

if typeOf == 1:
    db.execute("INSERT INTO students(uid, name, encoded_face) VALUES = ? ? ?", id, name, encoding_dump)
elif typeOf == 2:
    db.execute("INSERT INTO teaching_assistants(uid, name, encoded_face) VALUES = ? ? ?", id, name, encoding_dump)
else:
    raise("Invalid input for typeOf")