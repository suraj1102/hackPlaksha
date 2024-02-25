from utils import *
import time

db = sqlite3.connect("./data.db")

def class_exists (class_id : str = "") -> tuple :
    if class_id == "" : 
        print(f"Cannot create log for undefined class.")
        return -1
    
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
        return -1
        
    attendees_details = []
    
    cursor = db.cursor()
    cursor.execute("SELECT student_UID FROM Enrollment WHERE course_ID = ?", (lec_id,))
    attendees_details = [row[0] for row in cursor.fetchall()]

    if attendees_details == [] :
        print(f"No attendees found for lecture {lec_id}")

    attendees = []
    attendees_encodings = []

    return (attendees_encodings, attendees)

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

def start_capture (cam_id : int = 0, lecture_details : tuple = (), encoded_details : np.ndarray = np.array([])) :
    video_capture = get_video_stream(cam_id)

    while datetime.datetime.now() <= lecture_details[4]:

        timestamp, attendee_names = get_video_frame(video_capture, encoded_details)
        update_class_log(timestamp, lecture_details[0], attendee_names)
        time.sleep(1)
    
def end_lecture (lecture_details : tuple = ()) :
    
    #  fetch log from the DB and create a report in excel. Send to respeqctive faculty
    
    print(f"Ending Lecture {lecture_details[0]}")
    return 200

def start_lecture (class_id : str = "", cam_details : dict = {}, lecture_details : tuple = (), encoded_details : np.ndarray = np.array([])):
    
    if class_id == "" or cam_details == {} or lecture_details == () or encoded_details == np.array([]):
        print("Invalid Arguments: Cannot start lecture.")
        return 400

    for camera in cam_details:
        threading.Thread(target=start_capture, args=((camera, cam_details['camera']), lecture_details, encoded_details)).start()

    
if __name__ == "__main__":
    camera_details = tuple(get_camera_details())
    print(camera_details)

    class_id = camera_details[0]

    deployed = False

    while deployed:
        class_status = class_exists(class_id)

        if class_status[1]:
            lecture_details = (class_status[2], class_status[3], class_status[4])
            encoded_details = get_attendee_details(class_status[2])

            start_lecture(class_id, camera_details[1], lecture_details, encoded_details)

        