from dataclasses import dataclass

@dataclass
class Student:
    name: str
    email: str

@dataclass
class Course:
    course_name: str
    credits: int

@dataclass
class Enrollment:
    student_id: int
    course_id: int
    enrollment_date: str