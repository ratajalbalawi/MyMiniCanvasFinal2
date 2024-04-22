from unittest.mock import patch
import pytest #type:ignore
import main

# Fixtures
@pytest.fixture
def arranged_assignment():
    from assignment import Assignment
    my_assignment = Assignment(0, "4/22/2024", 0)
    return my_assignment

@pytest.fixture
def arranged_submission():
    from assignment import Submission
    my_submission = Submission(0, "Hello!")
    return my_submission

@pytest.fixture
def arranged_course():
    from course import Course
    my_course = Course(0, "COSC 381", "Winter", [arranged_teacher])
    my_course.import_students([arranged_student])
    return my_course

@pytest.fixture
def arranged_courseManager():
    from course import CourseManager
    my_courseManager = CourseManager()
    return my_courseManager

@pytest.fixture
def arranged_student():
    from user import User
    my_user = User(0, "Rataj Albalawi", "1234", "Student")
    return my_user

@pytest.fixture
def arranged_teacher():
    from user import User
    my_user = User(1, "Dr. Jiang", "4321", "Teacher")
    return my_user

@pytest.fixture
def arranged_userManager():
    from user import UserManager
    my_userManager = UserManager()
    return my_userManager

# ------------ assignment.py ------------
@patch("builtins.print")
def test_submit_assignment(mock_print, arranged_assignment, arranged_submission):
    # Act:
    arranged_assignment.submit(arranged_submission)
    arranged_assignment.submit("hello")

    # Assert:
    assert len(arranged_assignment.submission_list) == 1
    assert arranged_assignment.submission_list[0].submission == "Hello!"
    mock_print.assert_called_with("Submission error")

# ------------ course.py ------------
@patch("builtins.print")
def test_import_students(mock_print, arranged_course, arranged_student, arranged_teacher):
    # Act:
    arranged_course.import_students([arranged_student])
    arranged_course.import_students([arranged_student, arranged_teacher])
    mock_print.assert_called_with("Import error")
    arranged_course.import_students(["hello"])

    # Assert:
    assert len(arranged_course.student_list) == 1
    assert arranged_course.student_list[0].name == "Rataj Albalawi"
    mock_print.assert_called_with("Import error")
    
@patch("course.Course.generate_assignment_id", return_value=0)
@patch("builtins.print")
def test_create_an_assignment(mock_print, mock_generate_assignment_id, arranged_course):
    # Act:
    arranged_course.create_an_assignment("4/22/2024")
    arranged_course.create_an_assignment(42)

    # Assert:
    assert len(arranged_course.assignment_list) == 1
    assert arranged_course.assignment_list[0].assignment_id == 0
    mock_print.assert_called_with("Assignment creation error")

def test_generate_assignment_id(arranged_course):
    # Act:
    arranged_course.generate_assignment_id()
    arranged_course.generate_assignment_id()
    arranged_course.generate_assignment_id()

    # Assert:
    assert arranged_course.assignment_counter == 3

@patch("course.CourseManager.generate_id", return_value=0)
@patch("builtins.print")
def test_create_a_course(mock_print, mock_generate_id, arranged_courseManager, arranged_teacher, arranged_student):
    # Act:
    arranged_courseManager.create_a_course("COSC 381", "Winter", [arranged_teacher])
    arranged_courseManager.create_a_course("COSC 381", "Winter", [arranged_teacher, arranged_student])
    mock_print.assert_called_with("Course creation error")
    arranged_courseManager.create_a_course(42, "hello", "hello")

    # Assert:
    assert len(arranged_courseManager.course_list) == 1
    assert arranged_courseManager.course_list[0].course_code == "COSC 381"
    mock_print.assert_called_with("Course creation error")

def test_generate_id(arranged_courseManager):
    # Act:
    arranged_courseManager.generate_id()
    arranged_courseManager.generate_id()
    arranged_courseManager.generate_id()

    # Assert:
    assert arranged_courseManager.counter == 3

@patch("builtins.print")
def test_find_a_course(mock_print, arranged_courseManager, arranged_teacher):
    # Act:
    arranged_courseManager.create_a_course("COSC 381", "Winter", [arranged_teacher])
    arranged_courseManager.create_a_course("COSC 314", "Winter", [arranged_teacher])

    # Assert:
    assert arranged_courseManager.find_a_course(1) == arranged_courseManager.course_list[0]
    assert arranged_courseManager.find_a_course(5) == None
    arranged_courseManager.find_a_course("hello")
    mock_print.assert_called_with("Course search error")

# ------------ user.py ------------
def test_generate_id(arranged_userManager):
    # Act:
    arranged_userManager.generate_id()
    arranged_userManager.generate_id()
    arranged_userManager.generate_id()

    # Assert:
    assert arranged_userManager.counter == 3

@patch("user.UserManager.generate_id", return_value=0)
@patch("builtins.print")
def test_create_a_user(mock_print, mock_generate_id, arranged_userManager):
    # Act:
    arranged_userManager.create_a_user("Rataj Albalawi", "1234", "Student")
    arranged_userManager.create_a_user(42, "hello", "hello")

    # Assert:
    assert len(arranged_userManager.user_list) == 1
    assert arranged_userManager.user_list[0].name == "Gabe Karras"
    mock_print.assert_called_with("User creation error")

@patch("builtins.print")
def test_find_users(mock_print, arranged_userManager):
    # Act:
    arranged_userManager.create_a_user("Rataj Albalawi", "1234", "Student")
    arranged_userManager.create_a_user("Ammar Oweis", "12345", "Student")

    # Assert:
    assert arranged_userManager.find_users([1, 2])[1] == arranged_userManager.user_list[1]
    assert arranged_userManager.find_users([5]) == []
    arranged_userManager.find_users("goofy")
    mock_print.assert_called_with("User search error")

# ------------ main.py ------------
def test_welcome():
    #Assert:
    assert main.welcome() == "Welcome to our miniCanvas!"

def test_create_a_course_main(mocker, arranged_teacher, arranged_course):
    # Arrange:
    mock_find_users = mocker.patch("user.UserManager.find_users", return_value=[arranged_teacher])
    mock_create_a_course = mocker.patch("course.CourseManager.create_a_course", return_value=0)
    mock_find_a_course = mocker.patch("course.CourseManager.find_a_course", return_value=arranged_course)
    mock_print = mocker.patch("builtins.print")

    # Act:
    main.create_a_course("COSC 381", "Winter", [1])

    # Assert:
    mock_find_users.assert_called_with([1])
    mock_create_a_course.assert_called_with("COSC 381", "Winter", [arranged_teacher])
    mock_find_a_course.assert_called_with(0)
    mock_print.assert_called_with(str(arranged_course.teacher_list[0]))
    assert main.create_a_course("COSC 381", "Winter", [1]) == 0

def test_import_students_main(mocker, arranged_course, arranged_student):
    # Arrange:
    mock_find_a_course = mocker.patch("course.CourseManager.find_a_course", return_value=arranged_course)
    mock_find_users = mocker.patch("user.UserManager.find_users", return_value=[arranged_student])
    mock_import_students = mocker.patch("course.Course.import_students")
    mock_print = mocker.patch("builtins.print")

    # Act:
    main.import_students(1, [1])

    # Assert:
    mock_find_a_course.assert_called_with(1)
    mock_find_users.assert_called_with([1])
    mock_import_students.assert_called_with([arranged_student])
    mock_print.assert_has_calls([mocker.call(0), mocker.call(arranged_course.student_list)])
    assert main.import_students(1, [1]) == None