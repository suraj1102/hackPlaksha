CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    uid TEXT UNIQUE,
    name TEXT NOT NULL,
    encoded_face BLOB NOT NULL
);

CREATE TABLE teaching_assistants (
    id INTEGER PRIMARY KEY,
    assistant_id TEXT UNIQUE,
    name TEXT NOT NULL,
    encoding BLOB NOT NULL
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    course_code TEXT NOT NULL,
    name TEXT NOT NULL,
);

CREATE TABLE lectures (
    id INTEGER PRIMARY KEY,
    course_id TEXT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    day_of_lec TEXT NOT NULL CHECK(day_of_lec IN ('mo', 'tu', 'we', 'th', 'fr', 'sa', 'su')),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE student_enrollment (
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    -- PRIMARY KEY (student_id, course_id)
);

CREATE TABLE ta_enrollment (
    ta_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY (ta_id) REFERENCES teaching_assistants(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    -- PRIMARY KEY (ta_id, course_id)
);

CREATE TABLE logging (
    log_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    lecture_id INTEGER NOT NULL,
    last_entry DATETIME NOT NULL,
    time_spent FLOAT NOT NULL,
    recognition_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (lecture_id) REFERENCES lectures(id),
);