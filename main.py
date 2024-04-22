from fastapi import FastAPI
from typing import List
from course import CourseManager, Course
from user import UserManager
from fastapi.security import APIKeyHeader


coursemanager = CourseManager()
usermanager = UserManager()
usermanager.create_a_user("John", "pwd", "Studnet")
usermanager.create_a_user("Alice", "pwd", "Teacher")
usermanager.create_a_user("Jimmy", "pwd", "Admin")

app = FastAPI()

@app.get("/")
def welcome():
    return "Welcome to our miniCanvas!"

@app.post("/courses/{coursecode}")
def create_a_course(coursecode: str, 
                    semester: str, 
                    teacher_id_list: List[int]) -> int:
    ### an admin should create a course
    teacher_list = usermanager.find_users(teacher_id_list)
    if (len(teacher_list) == 0):
        print("Teacher id error")
        return -1
    
    course_id = coursemanager.create_a_course(coursecode, semester, teacher_list)
    
    course = coursemanager.find_a_course(course_id)
    print(str(course.teacher_list[0]))

    return course_id

@app.put("/courses/{courseid}/students")
def import_students(courseid: int,
                    student_id_list: List[int]) -> None:
    course = coursemanager.find_a_course(courseid)
    if (course == None):
        print("Course id error")
        return None

    student_list = usermanager.find_users(student_id_list)
    if (len(student_list) == 0):
        print("Student id error")
        return None

    course.import_students(student_list)
    
    print(course.course_id)
    print(course.student_list)
    
    return None