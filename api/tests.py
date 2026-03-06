from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import io

class UserCSVUploadTests(APITestCase):
    
    def setUp(self):
        self.url = reverse('user-upload') 

    def test_upload_valid_csv(self):
        csv_content = "name,email,age\nAlice,alice@test.com,30\nBob,bob@test.com,25"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = 'test.csv'
        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_saved'], 2)

    def test_duplicate_email_handling(self):
        csv_content = (
            "name,email,age\n"
            "Thomas,thomas@test.com,22\n"
            "Tom,thomas@test.com,21" 
        )
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = 'test.csv'
        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.data['total_saved'], 1)
        self.assertEqual(response.data['total_rejected'], 1)
        self.assertIn("already exists", str(response.data['validation_errors']))

    def test_invalid_age_constraint(self):
        csv_content = "name,email,age\nOld Man,old@test.com,150"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = 'test.csv'  
        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.data['total_rejected'], 1)

    def test_invalid_file_extension(self):
        file = io.BytesIO(b"name,email,age")
        file.name = 'test.txt' 
        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)