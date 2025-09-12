import pytest
from db_setup import initialize_db, reset_tables, get_connection
from models import Student, Course, Enrollment
from operations import (
    add_student,
    add_course,
    enroll_student,
    list_student_courses,
    course_report
)

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    initialize_db()

@pytest.fixture(autouse=True)
def clean_db():
    reset_tables()

def test_add_student():
    student = Student("John", "john@example.com")
    result = add_student(student)
    assert result is True

def test_add_duplicate_student():
    student = Student("John", "john@example.com")
    add_student(student)
    result = add_student(student)
    assert result is False

def test_add_course():
    course = Course("Python Programming", 4)
    add_course(course)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses WHERE course_name = %s", ("Python Programming",))
    assert cursor.fetchone() is not None
    conn.close()

def test_enroll_student_valid():
    student = Student("John", "john@example.com")
    course = Course("Python Programming", 4)
    add_student(student)
    add_course(course)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id FROM students WHERE email = %s", ("john@example.com",))
    sid = cursor.fetchone()[0]
    cursor.execute("SELECT course_id FROM courses WHERE course_name = %s", ("Python Programming",))
    cid = cursor.fetchone()[0]
    conn.close()

    enrollment = Enrollment(sid, cid, "2025-09-11")
    result = enroll_student(enrollment)
    assert result == "Enrollment successful"

def test_enroll_student_duplicate():
    student = Student("John", "john@example.com")
    course = Course("Python Programming", 4)
    add_student(student)
    add_course(course)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id FROM students WHERE email = %s", ("john@example.com",))
    sid = cursor.fetchone()[0]
    cursor.execute("SELECT course_id FROM courses WHERE course_name = %s", ("Python Programming",))
    cid = cursor.fetchone()[0]
    conn.close()

    enrollment = Enrollment(sid, cid, "2025-09-11")
    enroll_student(enrollment)
    result = enroll_student(enrollment)
    assert result == "Duplicate enrollment"

def test_list_student_courses():
    student = Student("John", "john@example.com")
    course = Course("Data Structures", 3)
    add_student(student)
    add_course(course)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id FROM students WHERE email = %s", ("john@example.com",))
    sid = cursor.fetchone()[0]
    cursor.execute("SELECT course_id FROM courses WHERE course_name = %s", ("Data Structures",))
    cid = cursor.fetchone()[0]
    conn.close()

    enrollment = Enrollment(sid, cid, "2025-09-11")
    enroll_student(enrollment)

    courses = list_student_courses(sid)
    assert len(courses) >= 1

def test_course_report():
    student = Student("John", "john@example.com")
    course1 = Course("Python Programming", 4)
    course2 = Course("Data Structures", 3)
    add_student(student)
    add_course(course1)
    add_course(course2)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id FROM students WHERE email = %s", ("john@example.com",))
    sid = cursor.fetchone()[0]
    cursor.execute("SELECT course_id FROM courses WHERE course_name = %s", ("Python Programming",))
    cid1 = cursor.fetchone()[0]
    cursor.execute("SELECT course_id FROM courses WHERE course_name = %s", ("Data Structures",))
    cid2 = cursor.fetchone()[0]
    conn.close()

    enroll_student(Enrollment(sid, cid1, "2025-09-11"))
    enroll_student(Enrollment(sid, cid2, "2025-09-12"))

    report = course_report()
    assert len(report) >= 2