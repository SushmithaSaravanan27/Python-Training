from db_setup import get_connection
from models import Student, Course, Enrollment
import mysql.connector

def add_student(student: Student):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (name, email) VALUES (%s, %s)", (student.name, student.email))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        conn.close()

def add_course(course: Course):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO courses (course_name, credits) VALUES (%s, %s)", (course.course_name, course.credits))
    conn.commit()
    conn.close()

def enroll_student(enrollment: Enrollment):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM students WHERE student_id = %s", (enrollment.student_id,))
    if not cursor.fetchone():
        conn.close()
        return "Invalid student ID"

    cursor.execute("SELECT 1 FROM courses WHERE course_id = %s", (enrollment.course_id,))
    if not cursor.fetchone():
        conn.close()
        return "Invalid course ID"

    try:
        cursor.execute("""
        INSERT INTO enrollments (student_id, course_id, enrollment_date)
        VALUES (%s, %s, %s)
        """, (enrollment.student_id, enrollment.course_id, enrollment.enrollment_date))
        conn.commit()
        return "Enrollment successful"
    except mysql.connector.IntegrityError:
        return "Duplicate enrollment"
    finally:
        conn.close()

def list_student_courses(student_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT c.course_name, c.credits, e.enrollment_date
    FROM enrollments e
    JOIN courses c ON e.course_id = c.course_id
    WHERE e.student_id = %s
    """, (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def course_report():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT c.course_name, s.name, s.email, e.enrollment_date
    FROM enrollments e
    JOIN students s ON e.student_id = s.student_id
    JOIN courses c ON e.course_id = c.course_id
    ORDER BY c.course_name
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows