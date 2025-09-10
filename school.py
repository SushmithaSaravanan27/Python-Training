import students 
import teachers 
import results 
id=int(input("Enter the student id:"))
name=input("Enter the student name:")
print(students.addStudents(id,name))
print(students.viewStudents())
id=int(input("Enter the teacher id:"))
sub=input("Enter the name of subject:")
print(teachers.assignSubject(id,sub))
print(teachers.viewTeachersInfo())
marks=int(input("Enter the marks:"))
print(results.calculateGrade(marks))
