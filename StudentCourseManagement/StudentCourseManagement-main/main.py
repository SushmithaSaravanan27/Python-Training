from db_setup import initialize_db
from models import Student, Course, Enrollment
from operations import add_student, add_course, enroll_student, list_student_courses, course_report

def menu():
    print("\nStudent Course Enrollment System")
    print("1. Add Student")
    print("2. Add Course")
    print("3. Enroll Student")
    print("4. List Student's Courses")
    print("5. Course-wise Report")
    print("6. Exit")

def main():
    initialize_db()
    while True:
        menu()
        choice = input("Enter choice: ").strip()
        if choice == "1":
            name = input("Student Name: ")
            email = input("Student Email: ")
            success = add_student(Student(name, email))
            print("Student added." if success else "Email already exists.")
        elif choice == "2":
            cname = input("Course Name: ")
            credits = int(input("Credits: "))
            add_course(Course(cname, credits))
            print("Course added.")
        elif choice == "3":
            sid = int(input("Student ID: "))
            cid = int(input("Course ID: "))
            date = input("Enrollment Date (YYYY-MM-DD): ")
            result = enroll_student(Enrollment(sid, cid, date))
            print(result)
        elif choice == "4":
            sid = int(input("Student ID: "))
            courses = list_student_courses(sid)
            if courses:
                for cname, credits, date in courses:
                    print(f"{cname} ({credits} credits) | Enrolled on: {date}")
            else:
                print("No courses found or invalid student ID.")
        elif choice == "5":
            report = course_report()
            if report:
                current_course = None
                for cname, sname, email, date in report:
                    if cname != current_course:
                        print(f"\n{cname}:")
                        current_course = cname
                    print(f"  - {sname} ({email}) | Enrolled on: {date}")
            else:
                print("No enrollments found.")
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()