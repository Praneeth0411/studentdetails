import unittest
from fastapi.testclient import TestClient
import main
from main import app


class TestStudentAPI(unittest.TestCase):
    """Test suite using Python's built-in unittest framework."""

    def setUp(self):
        """Reset in-memory database before each test run."""
        self.client = TestClient(app)
        main.students_db.clear()
        main.id_counter = 1

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Welcome to the Student Management API")

    def test_create_student_success(self):
        payload = {
            "name": "Rahul",
            "email": "rahul@gmail.com",
            "course": "Python Full Stack",
            "age": 22
        }
        response = self.client.post("/students", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], "Rahul")
        self.assertEqual(data["email"], "rahul@gmail.com")
        self.assertEqual(data["course"], "Python Full Stack")
        self.assertEqual(data["age"], 22)

    def test_create_student_invalid_email(self):
        payload = {
            "name": "Rahul",
            "email": "not-an-email",
            "course": "Python Full Stack",
            "age": 22
        }
        response = self.client.post("/students", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_create_student_invalid_age(self):
        payload = {
            "name": "Rahul",
            "email": "rahul@gmail.com",
            "course": "Python Full Stack",
            "age": -5
        }
        response = self.client.post("/students", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_create_student_empty_name(self):
        payload = {
            "name": "",
            "email": "rahul@gmail.com",
            "course": "Python Full Stack",
            "age": 22
        }
        response = self.client.post("/students", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_create_student_already_exists(self):
        payload = {
            "name": "Rahul",
            "email": "rahul@gmail.com",
            "course": "Python Full Stack",
            "age": 22
        }
        # First creation succeeds
        first_res = self.client.post("/students", json=payload)
        self.assertEqual(first_res.status_code, 201)

        # Duplicate creation should be rejected
        duplicate_res = self.client.post("/students", json=payload)
        self.assertEqual(duplicate_res.status_code, 400)
        self.assertEqual(duplicate_res.json()["detail"], "Student already exists.")

    def test_get_all_students(self):
        self.client.post("/students", json={"name": "Rahul", "email": "rahul@gmail.com", "course": "Python Full Stack", "age": 22})
        self.client.post("/students", json={"name": "Priya", "email": "priya@gmail.com", "course": "Data Science", "age": 24})

        response = self.client.get("/students")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], 1)
        self.assertEqual(data[1]["id"], 2)

    def test_get_student_by_id_success(self):
        self.client.post("/students", json={"name": "Rahul", "email": "rahul@gmail.com", "course": "Python Full Stack", "age": 22})
        response = self.client.get("/students/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], "Rahul")

    def test_get_student_by_id_not_found(self):
        response = self.client.get("/students/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Student not found")

    def test_update_student_success(self):
        self.client.post("/students", json={"name": "Rahul", "email": "rahul@gmail.com", "course": "Python Full Stack", "age": 22})
        update_payload = {
            "name": "Rahul Sharma",
            "email": "rahul.sharma@gmail.com",
            "course": "AI & ML",
            "age": 23
        }
        response = self.client.put("/students/1", json=update_payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], "Rahul Sharma")
        self.assertEqual(data["course"], "AI & ML")

    def test_update_student_not_found(self):
        update_payload = {
            "name": "Ghost",
            "email": "ghost@gmail.com",
            "course": "DevOps",
            "age": 30
        }
        response = self.client.put("/students/999", json=update_payload)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Student not found")

    def test_delete_student_success(self):
        self.client.post("/students", json={"name": "Rahul", "email": "rahul@gmail.com", "course": "Python Full Stack", "age": 22})
        response = self.client.delete("/students/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Student deleted successfully")

        # Verify record is removed
        get_res = self.client.get("/students/1")
        self.assertEqual(get_res.status_code, 404)

    def test_delete_student_not_found(self):
        response = self.client.delete("/students/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Student not found")

    def test_bonus_search_by_course(self):
        self.client.post("/students", json={"name": "Rahul", "email": "rahul@gmail.com", "course": "Python Full Stack", "age": 22})
        self.client.post("/students", json={"name": "Aman", "email": "aman@gmail.com", "course": "Advanced Python", "age": 25})
        self.client.post("/students", json={"name": "Priya", "email": "priya@gmail.com", "course": "Java Spring Boot", "age": 23})

        # Search for "python" (case-insensitive partial match)
        response = self.client.get("/students/search?course=Python")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        names = {s["name"] for s in data}
        self.assertEqual(names, {"Rahul", "Aman"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
