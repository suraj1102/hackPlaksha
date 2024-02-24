from utils import *
import time

def class_exists (class_id : str = "") -> tuple :
    if class_id == "" : 
        print(f"Cannot create log for undefined class.")

    # Insert SQL Query here!
    '''
        Query to check if the class has a scheduled lecture. 
    '''
    
    class_data = None

    if class_data == None :
        return (class_id, False)
    else :
        return (class_id, True, class_data["lec_id"], class_data["start_time"], class_data["end_time"])

def get_attendee_details (lec_id : str = "") -> list :
    if lec_id == "" : 
        print(f"Cannot create log for undefined class.")

    attendees = []

    # Insert SQL Query here!
    '''
        Query to get the attendees UID for a specific lecture (with lec_id).
    '''

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
        image = face_recognition.load_image_file(IMAGE_DB_PATH + attendee)
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

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    attendee_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(encoded_details[:,0], face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = encoded_details[:,first_matchindex]

        attendee_names.append(name)
    
    return (timestamp, attendee_names)

def update_class_log (timestamp : datetime.datetime, mode : str = "entry", attendee_names : list = []) -> int :
    # Insert SQL Query here!
    '''
        Query to update the class log with the attendance data.
    '''

    return 0

def start_capture (cam_idx : int = 0, lecture_details : tuple, encoded_details : np.ndarray = np.array([])) :
    video_capture = get_video_stream(cam_idx)

    while time.now() <= lecture_details[4]:

        timestamp, attendee_names = get_video_frame(video_capture, encoded_details)
        update_class_log(timestamp, mode, attendee_names)
        time.sleep(5)
    

def main () :
    pass