from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User

# Create your tests here.
class AccountsTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test2@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
            role='buyer',
            is_verified = True
        )

    def test_user_registration(self):
        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'buyer',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        users = User.objects.filter(email='test@example.com')
        self.assertEqual(users.count(), 1)


    def test_user_registration_invalid(self):
        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'password': '',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'buyer',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_user_registration_existing_email(self):
        url = reverse('register')
        data = {
            'email': 'test2@example.com',
            'password': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'buyer',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test2@example.com')

    def test_user_login(self):
        url = reverse('token-obtain-pair')
        data = {
            'email': 'test2@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_invalid_credentials(self):
        url = reverse('token-obtain-pair')
        data = {
            'email': 'example@gmail.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        