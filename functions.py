from utils import *
import face_recognition
import time

db = sqlite3.connect("./data.db")

def class_exists (class_id : str = "") -> tuple :
    if class_id == "" : 
        print(f"Cannot create log for undefined class.")
        return class_id, False
    
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Lecture WHERE ID = ?", (class_id,))
    class_data = cursor.fetchone()

    if class_data == None :
        return (class_id, False)
    else :
        return (class_id, True, class_data["lec_id"], class_data["start_time"], class_data["end_time"])

def get_attendee_details (lec_id : str = "") -> list :
    if lec_id == "" : 
        print(f"Cannot create log for undefined class.")
        return []

    attendees = []
    cursor = db.cursor()
    cursor.execute("SELECT student_UID FROM Enrollment WHERE course_ID = ?", (lec_id,))
    attendees = [row[0] for row in cursor.fetchall()]

    if attendees == [] :
        print(f"No attendees found for lecture {lec_id}")

    return attendees

def encode_attendees (attendees : list = []) -> tuple :
    if attendees == [] : 
        print("Empty Session: Session cannot be empty!")

    attendee_face_encodings = []
    attendee_face_names = []

    for attendee in attendees:
        attendee_image = 'Attendee Image from DB' # Run SQL Query to get the image of the attendee
        image = face_recognition.load_image_file(attendee_image)
        face_encoding = face_recognition.face_encodings(image)[0]

        attendee_face_encodings.append(face_encoding)
        attendee_face_names.append(attendee.split('.')[:-1])

    return np.array([(attendee_face_encodings[idx], attendee_face_names[idx]) for idx in range(len(attendees))])

def get_video_stream (idx : int = 0) -> cv2.VideoCapture:
    return cv2.VideoCapture(idx)

def get_video_frame (video_capture : cv2.VideoCapture, encoded_details : np.ndarray) -> tuple :
    ret, frame = video_capture.read()
    timestamp = datetime.datetime.now()
    
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

    face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    attendee_ids = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(encoded_details[:,0], face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = encoded_details[:,first_match_index]

        attendee_ids.append(name)
    
    return (timestamp, attendee_ids)

def update_class_log (timestamp : datetime.datetime, lecture_ID : str, mode : str = "entry", attendee_names : list = []) -> int :
    cursor = db.cursor()
    for student_ID in attendee_names:
        cursor.execute("INSERT INTO Logging (student_ID, lecture_ID, last_entry, time_spent) VALUES (?, ?, ?, ?)",
                       (student_ID, lecture_ID, timestamp, 0))
    db.commit()

    return 200

def start_capture (cam_details : tuple = (), lecture_details : tuple = (), encoded_details : np.ndarray = np.array([])) :
    video_capture = get_video_stream(cam_details[0])

    while datetime.datetime.now() <= lecture_details[4]:

        timestamp, attendee_names = get_video_frame(video_capture, encoded_details)
        update_class_log(timestamp, cam_details[1], attendee_names)
        time.sleep(1)
    
def start_lecture (class_id : str = ""):
    class_info = class_exists(class_id)
    if not class_info[1]:
        print("Lecture does not exist.")
        return

    # Retrieve lecture details
    lecture_id = class_info[2]
    start_time = class_info[3]
    end_time = class_info[4]

    # Get attendee details
    attendees = get_attendee_details(lecture_id)

    # Encode attendee information
    encoded_details = encode_attendees(attendees)

    # Start capturing video and processing attendance
    video_capture = get_video_stream()
    while datetime.datetime.now() <= end_time:
        timestamp, attendee_names = get_video_frame(video_capture, encoded_details)
        update_class_log(timestamp, "entry", attendee_names)
        time.sleep(1)

    print("Lecture ended.")


if __name__ == "__main__":
    # camera_details = tuple(get_camera_details())
    # print(camera_details)
    class_id = input("Enter the ID of the lecture to start: ")
    start_lecture(class_id)
