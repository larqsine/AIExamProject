import unittest
from fastapi.testclient import TestClient
import io
import os

from main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        
    def test_upload_cv_txt(self):
        file_content = b"This is a test CV.\nI have experience in Python programming."
        response = self.client.post(
            "/api/v1/upload/cv",
            files={"file": ("test_cv.txt", io.BytesIO(file_content), "text/plain")}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("text", data)
        
    def test_feedback_endpoint(self):
        test_cv = "I have 5 years of experience in Python programming."
        response = self.client.post(
            "/api/v1/feedback",
            json={"text": test_cv, "feedback_type": "grammar"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("feedback", data)