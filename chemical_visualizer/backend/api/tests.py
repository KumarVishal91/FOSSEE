from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Dataset


class DatasetAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_upload_csv(self):
        csv_content = b"Equipment Name,Type,Flowrate,Pressure,Temperature\nPump A,Pump,120.5,3.2,65\n"
        csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")

        response = self.client.post("/api/upload/", {"file": csv_file}, format="multipart")
        self.assertEqual(response.status_code, 200)
        self.assertIn("summary", response.data)
        self.assertEqual(Dataset.objects.count(), 1)

    def test_upload_invalid_csv(self):
        csv_content = b"Invalid,Header\nData,More Data\n"
        csv_file = SimpleUploadedFile("invalid.csv", csv_content, content_type="text/csv")

        response = self.client.post("/api/upload/", {"file": csv_file}, format="multipart")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_history_endpoint(self):
        response = self.client.get("/api/history/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_authentication_required(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/history/")
        self.assertEqual(response.status_code, 403)
