import face_recognition
import cv2
import numpy as np 

video_capture = cv2.VideoCapture(0)

suraj_image = face_recognition.load_image_file("suraj.jpg")
suraj_face_encoding = face_recognition.face_encodings(suraj_image)[0]

vaisakh_image = face_recognition.load_image_file("vaisakh.png")
vaisakh_face_encoding = face_recognition.face_encodings(vaisakh_image)[0]

manan_image = face_recognition.load_image_file("manan.png")
manan_face_encoding = face_recognition.face_encodings(manan_image)[0]

gaurav_image = face_recognition.load_image_file("gaurav.png")
gaurav_face_encoding = face_recognition.face_encodings(gaurav_image)[0]


known_face_encodings = [
    suraj_face_encoding,
    vaisakh_face_encoding,
    manan_face_encoding,
    gaurav_face_encoding
]
known_face_names = [
    "Suraj",
    "Vaisakh",
    "Manan",
    "Gaurav"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()
    
    if process_this_frame:
        
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)    
    
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()