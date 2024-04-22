from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from main import usermanager

client = TestClient(app)

def test_welcome_API():
    # Act:
    response = client.get("/")

    # Assert:
    assert(response.status_code == 200)
    assert(response.json() == "Welcome to our miniCanvas!")

@patch("builtins.print")
def test_create_a_course_API(mock_print):
    # Act:
    response1 = client.post("/courses/COSC%20381?semester=Winter",
                           headers={"accept": "application/json", "Content-Type": "application/json"},
                           json=[2])
    response2 = client.post("/courses/COSC%20381?semester=Winter",
                           headers={"accept": "application/json", "Content-Type": "application/json"},
                           json=[5])

    # Assert:
    assert(response1.status_code == 200)
    assert(response1.json() == 1)
    assert(response2.status_code == 200)
    assert(response2.json() == -1)
    mock_print.assert_called_with("Teacher id error")

def test_import_students_API(mocker):
    # Arrange:
    mock_print = mocker.patch("builtins.print")
    
    # Act:
    response1 = client.put("/courses/1/students", 
                            headers={"accept": "application/json", "Content-Type": "application/json"}, 
                            json=[1])
    response2 = client.put("/courses/2/students", 
                            headers={"accept": "application/json", "Content-Type": "application/json"}, 
                            json=[1])
    mock_print.assert_called_with("Course id error")
    response3 = client.put("/courses/1/students", 
                            headers={"accept": "application/json", "Content-Type": "application/json"}, 
                            json=[5])
    
    # Assert:
    assert(response1.status_code == 200)
    assert(response2.status_code == 200)
    assert(response3.status_code == 200)
    mock_print.assert_called_with("Student id error")