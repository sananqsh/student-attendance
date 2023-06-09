import sqlite3
from datetime import timedelta, datetime
from random import randint, randrange

conn = sqlite3.connect('attendance.db')
c = conn.cursor()

TABLES = ["students", "teachers", "lessons", "courses", "registrations", "sessions", "session_attendances"]
COURSES_START = datetime.strptime('1/4/2023 7:30 AM', '%m/%d/%Y %I:%M %p')
COURSES_END = datetime.strptime('1/6/2023 8:00 PM', '%m/%d/%Y %I:%M %p')

def create_tables():
    c.execute('''
    CREATE TABLE IF NOT EXISTS students
    ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [name] TEXT, [student_number] TEXT)
    ''')

    # ex: Calculus I, Chemistry, etc.
    c.execute('''
    CREATE TABLE IF NOT EXISTS lessons
    ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [name] TEXT)
    ''')


    c.execute('''
    CREATE TABLE IF NOT EXISTS teachers
    ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [name] TEXT)
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS courses
    ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [lesson_id] INTEGER, [teacher_id] INTEGER, FOREIGN KEY(lesson_id) REFERENCES lessons(id), FOREIGN KEY(teacher_id) REFERENCES teachers(id))
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS sessions
    ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [course_id] INTEGER, [session_time] date, FOREIGN KEY(course_id) REFERENCES courses(id))
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS registrations
    ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [course_id] INTEGER, [student_id] INTEGER, FOREIGN KEY(course_id) REFERENCES courses(id), FOREIGN KEY(student_id) REFERENCES students(id))
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS session_attendances
    ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [student_id] INTEGER, [session_id] INTEGER, [presence] BOOLEAN DEFAULT 0, FOREIGN KEY(session_id) REFERENCES sessions(id), FOREIGN KEY(student_id) REFERENCES students(id))
    ''')


def select_from(table, where_clause=None, column = "id"):
    q = "SELECT " + column + " FROM "

    if table in TABLES:
        q += table
    else:
        print("Not a valid table!")
        return None

    if where_clause:
        q += " WHERE " + where_clause

    sqlite_result = c.execute(q)

    return [row[0] for row in sqlite_result]


def feed():
    student_names = ["امید", "رویا", "هوشنگ", "ترانه", "الهام", "ژینا", "نیما", "متین", "شهاب", "بهنام", "بیژن", "پریا", "پارسا", "هیمن"]
    teacher_names = ["یدالله", "نیلوفر", "مصطفی", "یاسر", "ریحانه", "رضا", "روژین", "شهرزاد", "نگار", "امیرمحمد", "الناز", "اسرا", "صادق جان"]
    lesson_names = ["ریاضی ۱", "ریاضی ۲", "فیزیک ۱", "فیزیک ۲", "شیمی ۱", "معادلات دیفرانسیل", "برنامه نویسی کامپیوتر"]

    feed_students(student_names)
    print("-STUDENTS DONE")
    feed_teachers(teacher_names)
    print("-TEACHERS DONE")
    feed_lessons(lesson_names)
    print("-LESSONS DONE")
    feed_courses()
    print("-COURSES DONE")
    feed_sessions()
    print("-SESSIONS DONE")
    feed_registrations()
    print("-REGISTRATIONS DONE")
    feed_session_attendances()
    print("-SESSION_ATTENDANCES DONE")

def update_session_attendance(student_number, session_id):
    student_id = select_from("students", f"student_number={student_number}")

    session_attendance = c.execute('''
    SELECT id, presence FROM session_attendances WHERE session_id = (?) AND student_id = (?)
    ''', (session_id, student_id))

    if session_attendance:
        r = [row for row in session_attendance]

        id, presence = r[0][0], r[0][1]

        if presence == 0:
            print("ABSENT")
            # update in db
            c.execute('''
            UPDATE session_attendances SET presence=1 WHERE id = (?)
            ''', [id])

            conn.commit()
            return 0
        else:
            print("INCLASS")
            return 2
    else:
        return 1


def feed_students(names):
    rand_top_idx = len(names) - 1
    for _ in range(10):
        name = names[randint(0, rand_top_idx)]
        student_number = generate_random_student_number()
        c.execute('''INSERT INTO students (name, student_number) VALUES (?,?)''', (name, student_number))
        conn.commit()


def feed_teachers(names):
    for name in names:
        c.execute('''INSERT INTO teachers (name) VALUES (?)''', (name,))
        conn.commit()


def feed_lessons(names):
    for name in names:
        c.execute('''INSERT INTO lessons (name) VALUES (?)''', (name,))
        conn.commit()


def feed_courses():
    teacher_ids = select_from("teachers")
    lesson_ids = select_from("lessons")

    for i in range(5):
        c.execute('''INSERT INTO courses (teacher_id, lesson_id) VALUES (?, ?)''', (teacher_ids[i], lesson_ids[i]))
        conn.commit()


def feed_sessions():
    course_ids = select_from("courses")

    for course_id in course_ids:
        for i in range(5):
            time = random_date(COURSES_START, COURSES_END)
            c.execute('''INSERT INTO sessions (course_id, session_time) VALUES (?, ?)''', (course_ids[i], time))
            conn.commit()


def feed_registrations():
    student_ids = select_from("students")
    course_ids = select_from("courses")

    for i in range(10):
        c.execute('''INSERT INTO registrations (student_id, course_id) VALUES (?, ?)''', (student_ids[i], course_ids[i % len(course_ids)]))
        conn.commit()


def feed_session_attendances():
    course_ids = select_from("courses")

    for course_id in course_ids:
        student_ids = select_from("registrations", f"course_id={course_id}", column="student_id")
        session_ids = select_from("sessions", f"course_id={course_id}")

        for session_id in session_ids:
            for student_id in student_ids:
                c.execute('''INSERT INTO session_attendances (student_id, session_id) VALUES (?, ?)''', (student_id, session_id))
                conn.commit()


def generate_random_student_number():
    """
    Return a random Fanni student number.
    """
    fanni_school = "81"
    specialization_school = "{:02d}".format(randint(1, 9))
    enroll_year = str(randint(1394, 1402))[2:4]
    last_id_chunk = "{:03d}".format((randint(0, 120)))

    return int(fanni_school + specialization_school + enroll_year + last_id_chunk)


def random_date(start, end):
    """
    Return a random datetime between two datetime objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)

    return start + timedelta(seconds=random_second)
