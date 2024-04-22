from assignment import Assignment
from user import User

class CourseManager:
    def __init__(self):
        self.course_list = []
        self.counter = 0

    def create_a_course(self, course_code, semester, teacher_list):
        if (type(course_code) != str or type(semester) != str or type(teacher_list) != list):
            print("Course creation error")
            return
        else:
            for item in teacher_list:
                if (type(item) != User or item.type != "Teacher"):
                    print("Course creation error")
                    return

        ## automatically generate a courseId
        new_course_id = self.generate_id()
        new_course = Course(new_course_id, course_code, semester, teacher_list)

        # add the new course to the list
        self.course_list.append(new_course)
        return new_course_id

    def generate_id(self):
        self.counter += 1
        return self.counter

    def find_a_course(self, id):
        if (type(id) != int):
            print("Course search error")
            return

        print(f"target id: {id}")
        for course in self.course_list:
            print(f"course: {course.course_id}")
            if course.course_id == id:
                return course
            
        return None

    def sync_with_database(self):
        # will not implement here
        pass

class Course:
    def __init__(self, course_id, course_code, semester, teacher_list):
        self.course_id = course_id
        self.course_code = course_code
        self.semester = semester
        self.teacher_list = teacher_list
        self.student_list = []
        self.assignment_list = []
        self.module_list = []
        self.assignment_counter = 0

    def import_students(self, student_list):
        if (type(student_list) != list):
            print("Import error")
            return
        else:
            for item in student_list:
                if (type(item) != User or item.type != "Student"):
                    print("Import error")
                    return

        # the admin should import the students to a course
        self.student_list = student_list
    
    def create_an_assignment(self, due_date):
        if (type(due_date) != str):
            print("Assignment creation error")
            return

        new_assignment_id = self.generate_assignment_id()
        new_assignment = Assignment(new_assignment_id, 
                                    due_date, self.course_id)
        self.assignment_list.append(new_assignment)
    
    def generate_assignment_id(self):
        self.assignment_counter += 1
        return self.assignment_counter

    def __str__(self) -> str:
        return f"ID: {self.course_id}, code: {self.course_code}, teachers: {self.teacher_list}. students: {self.student_list}"