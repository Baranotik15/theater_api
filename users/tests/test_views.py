from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("user-register")
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        }

    def test_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post(
            self.register_url,
            self.user_data,
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            User.objects.count(),
            1
        )
        user = User.objects.first()
        self.assertEqual(
            user.username,
            self.user_data["username"]
        )
        self.assertEqual(
            user.email,
            self.user_data["email"]
        )
        self.assertTrue(
            "detail" in response.data
        )
        self.assertEqual(
            response.data["username"],
            self.user_data["username"]
        )

    def test_user_registration_without_email(self):
        """Test registration without email """
        data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = self.client.post(
            self.register_url,
            data,
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            User.objects.count(),
            1
        )

    def test_user_registration_invalid_password(self):
        """Test registration with invalid password"""
        data = self.user_data.copy()
        data["password"] = "123"
        response = self.client.post(
            self.register_url,
            data,
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertTrue(
            "password" in response.data["errors"]
        )
        self.assertEqual(
            User.objects.count(),
            0
        )

    def test_user_registration_invalid_username(self):
        """Test registration with invalid username"""
        data = self.user_data.copy()
        data["username"] = "ab"
        response = self.client.post(
            self.register_url,
            data,
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertTrue(
            "username" in response.data["errors"]
        )
        self.assertEqual(
            User.objects.count(),
            0
        )

    def test_user_registration_duplicate_username(self):
        """Test registration with duplicate username"""
        self.client.post(
            self.register_url,
            self.user_data,
            format="json"
        )

        duplicate_data = self.user_data.copy()
        duplicate_data["email"] = "another@example.com"
        response = self.client.post(
            self.register_url,
            duplicate_data,
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertTrue(
            "username" in response.data["errors"]
        )
        self.assertEqual(
            User.objects.count(),
            1
        )
