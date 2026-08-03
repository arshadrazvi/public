import unittest
import requests

BASE_URL = "http://127.0.0.1:5001"


class CodeCraftHubAPITest(unittest.TestCase):

    created_course_id = None

    # ----------------------------
    # Root Endpoint
    # ----------------------------
    def test_01_root(self):
        response = requests.get(f"{BASE_URL}/")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("message", data)

    # ----------------------------
    # Get All Courses
    # ----------------------------
    def test_02_get_all_courses(self):
        response = requests.get(f"{BASE_URL}/api/courses")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    # ----------------------------
    # Create Course
    # ----------------------------
    def test_03_create_course(self):
        payload = {
            "name": "Python Fundamentals",
            "description": "Learn Python from scratch.",
            "target_date": "2026-12-31",
            "status": "Not Started"
        }

        response = requests.post(
            f"{BASE_URL}/api/courses",
            json=payload
        )

        self.assertEqual(response.status_code, 201)

        data = response.json()

        self.assertEqual(data["name"], payload["name"])
        self.assertEqual(data["description"], payload["description"])
        self.assertEqual(data["target_date"], payload["target_date"])
        self.assertEqual(data["status"], payload["status"])

        CodeCraftHubAPITest.created_course_id = data["id"]

    # ----------------------------
    # Get Course by ID
    # ----------------------------
    def test_04_get_course(self):
        course_id = CodeCraftHubAPITest.created_course_id

        response = requests.get(
            f"{BASE_URL}/api/courses/{course_id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], course_id)

    # ----------------------------
    # Update Course
    # ----------------------------
    def test_05_update_course(self):
        course_id = CodeCraftHubAPITest.created_course_id

        payload = {
            "name": "Advanced Python",
            "description": "Master Python programming.",
            "target_date": "2027-01-15",
            "status": "In Progress"
        }

        response = requests.put(
            f"{BASE_URL}/api/courses/{course_id}",
            json=payload
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["name"], payload["name"])
        self.assertEqual(data["status"], "In Progress")

    # ----------------------------
    # Delete Course
    # ----------------------------
    def test_06_delete_course(self):
        course_id = CodeCraftHubAPITest.created_course_id

        response = requests.delete(
            f"{BASE_URL}/api/courses/{course_id}"
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["message"], "Deleted")
        self.assertEqual(data["id"], course_id)

    # ----------------------------
    # Verify Deleted
    # ----------------------------
    def test_07_verify_deleted(self):
        course_id = CodeCraftHubAPITest.created_course_id

        response = requests.get(
            f"{BASE_URL}/api/courses/{course_id}"
        )

        self.assertEqual(response.status_code, 404)

    # ======================================================
    # Error Tests
    # ======================================================

    def test_08_post_missing_field(self):
        payload = {
            "name": "Flask",
            "description": "API Development",
            "status": "Not Started"
        }

        response = requests.post(
            f"{BASE_URL}/api/courses",
            json=payload
        )

        self.assertEqual(response.status_code, 400)

    def test_09_post_invalid_status(self):
        payload = {
            "name": "Flask",
            "description": "API",
            "target_date": "2026-12-31",
            "status": "Finished"
        }

        response = requests.post(
            f"{BASE_URL}/api/courses",
            json=payload
        )

        self.assertEqual(response.status_code, 400)

    def test_10_post_invalid_date(self):
        payload = {
            "name": "Java",
            "description": "Programming",
            "target_date": "31-12-2026",
            "status": "Not Started"
        }

        response = requests.post(
            f"{BASE_URL}/api/courses",
            json=payload
        )

        self.assertEqual(response.status_code, 400)

    def test_11_post_empty_payload(self):
        response = requests.post(
            f"{BASE_URL}/api/courses"
        )

        self.assertEqual(response.status_code, 400)

    def test_12_get_course_not_found(self):
        response = requests.get(
            f"{BASE_URL}/api/courses/9999"
        )

        self.assertEqual(response.status_code, 404)

    def test_13_update_course_not_found(self):
        payload = {
            "name": "React",
            "description": "Frontend",
            "target_date": "2026-12-31",
            "status": "Completed"
        }

        response = requests.put(
            f"{BASE_URL}/api/courses/9999",
            json=payload
        )

        self.assertEqual(response.status_code, 404)

    def test_14_delete_course_not_found(self):
        response = requests.delete(
            f"{BASE_URL}/api/courses/9999"
        )

        self.assertEqual(response.status_code, 404)

    def test_15_put_missing_fields(self):
        payload = {
            "name": "Only Name"
        }

        response = requests.put(
            f"{BASE_URL}/api/courses/1",
            json=payload
        )

        self.assertEqual(response.status_code, 400)

    def test_16_put_invalid_status(self):
        payload = {
            "name": "Python",
            "description": "Programming",
            "target_date": "2026-12-31",
            "status": "Done"
        }

        response = requests.put(
            f"{BASE_URL}/api/courses/1",
            json=payload
        )

        self.assertEqual(response.status_code, 400)

    def test_17_put_invalid_date(self):
        payload = {
            "name": "Python",
            "description": "Programming",
            "target_date": "12/31/2026",
            "status": "Completed"
        }

        response = requests.put(
            f"{BASE_URL}/api/courses/1",
            json=payload
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main(verbosity=2)
