import sqlite3
from datetime import timedelta, datetime
from random import randint, randrange

conn = sqlite3.connect('attendance.db')
c = conn.cursor()

TABLES = ["student", "teacher", "lesson", "course", "registration", "session"]
COURSES_START = datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
COURSES_END = datetime.strptime('1/1/2009 4:50 AM', '%m/%d/%Y %I:%M %p')

def create_tables():
    c.execute('''
    CREATE TABLE IF NOT EXISTS student
    ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [name] TEXT, [number] TEXT)
    ''')

    # ex: Calculus I, Chemistry, etc.
    c.execute('''
    CREATE TABLE IF NOT EXISTS lesson
    ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [name] TEXT)
    ''')


    c.execute('''
    CREATE TABLE IF NOT EXISTS teacher
    ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [name] TEXT)
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS course
    ([id] INTEGER PRIMARY KEY AUTOINCREMENT, lesson_id INTEGER, teacher_id INTEGER, FOREIGN KEY(lesson_id) REFERENCES lessons(id), FOREIGN KEY(teacher_id) REFERENCES teachers(id))
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS session
    ([id] INTEGER PRIMARY KEY AUTOINCREMENT, course_id INTEGER, [session_time] date, FOREIGN KEY(course_id) REFERENCES courses(id))
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS registration
    ([id] INTEGER PRIMARY KEY AUTOINCREMENT, course_id INTEGER, student_id INTEGER, FOREIGN KEY(course_id) REFERENCES courses(id), FOREIGN KEY(student_id) REFERENCES students(id))
    ''')

def select_ids_from(table):
    if table == "student":
        sqlite_result = c.execute('''SELECT id FROM student''')
    elif table == "teacher":
        sqlite_result = c.execute('''SELECT id FROM teacher''')
    elif table == "lesson":
        sqlite_result = c.execute('''SELECT id FROM lesson''')
    elif table == "course":
        sqlite_result = c.execute('''SELECT id FROM course''')
    elif table == "registration":
        sqlite_result = c.execute('''SELECT id FROM registration''')
    elif table == "session":
        sqlite_result = c.execute('''SELECT id FROM session''')
    else:
        print("Not a valid table!")
        return None

    return [row[0] for row in sqlite_result]

def feed():
    student_names = ["امید", "رویا", "هوشنگ", "ترانه", "الهام", "ژینا", "نیما", "راهین", "شهاب", "بهنام", "بیژن", "پریا", "پارسا", "هیمن"]
    teacher_names = ["یدالله", "نیلوفر", "مصطفی", "یاسر", "ریحانه", "رضا", "روژین", "شهرزاد", "نگار", "امیرمحمد", "الناز", "اسرا", "صادق جان"]
    lesson_names = ["ریاضی ۱", "ریاضی ۲", "فیزیک ۱", "فیزیک ۲", "شیمی ۱", "معادلات دیفرانسیل", "برنامه نویسی کامپیوتر"]

    # feed_students(student_names)
    # feed_teachers(teacher_names)
    # feed_lessons(lesson_names)
    # feed_courses()
    feed_sessions()

def feed_students(names):
    rand_top_idx = len(names) - 1
    for _ in range(10):
        name = names[randint(0, rand_top_idx)]
        student_number = generate_random_student_number()
        c.execute('''INSERT INTO student (name, number) VALUES (?,?)''', (name, student_number))
        conn.commit()


def feed_teachers(names):
    for name in names:
        c.execute('''INSERT INTO teacher (name) VALUES (?)''', (name,))
        conn.commit()


def feed_lessons(names):
    for name in names:
        c.execute('''INSERT INTO lesson (name) VALUES (?)''', (name,))
        conn.commit()


def feed_courses():
    teacher_ids = select_ids_from("teacher")
    lesson_ids = select_ids_from("lesson")

    for i in range(5):
        c.execute('''INSERT INTO course (teacher_id, lesson_id) VALUES (?, ?)''', (teacher_ids[i], lesson_ids[i]))
        conn.commit()


def feed_sessions():
    course_ids = select_ids_from("course")

    for course_id in course_ids:
        for i in range(6):
            time = random_date(COURSES_START, COURSES_END)
            c.execute('''INSERT INTO course (teacher_id, lesson_id) VALUES (?, ?)''', (teacher_ids[i], lesson_ids[i]))
            conn.commit()
            # print(time)


def generate_random_student_number():
    fanni_school = "81"
    specialization_school = "{:02d}".format(randint(1, 9))
    enroll_year = str(randint(1394, 1402))[2:4]
    last_chunk_id = "{:03d}".format((randint(0, 120)))

    return int(fanni_school + specialization_school + enroll_year + last_chunk_id)


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)

    return start + timedelta(seconds=random_second)


# jdatetime.datetime.fromgregorian(datetime=datetime.datetime.now()).strftime("%a, %d %b %Y %H:%M:%S")
