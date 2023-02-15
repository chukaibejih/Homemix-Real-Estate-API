from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Referral

# Create your tests here.
class AccountsTest(APITestCase):

    def setUp(self):
            self.user = User.objects.create_user(
                email='test2@example.com',
                password='testpassword',
                first_name='John',
                last_name='Doe',
                role='buyer',
                referral_code = 'HM-4UKCzY',
                is_verified = True
            )
            self.referral = Referral.objects.create(
                referrer=self.user,
                referred=self.user,
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

    def test_user_registration_with_referral_code(self):
            url = reverse('register')
            data = {
                'email': 'test@example.com',
                'password': 'testpassword',
                'first_name': 'John',
                'last_name': 'Doe',
                'role': 'buyer',
                'referral_code': 'HM-4UKCzY'
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(User.objects.count(), 2)

            # Test that referral object is created correctly
            new_user = User.objects.get(email='test@example.com')
            new_referral = Referral.objects.get(referred=new_user)
            self.assertEqual(new_referral.referrer, self.user)

    def test_user_registration_without_referral_code(self):
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
        self.assertEqual(User.objects.count(), 2)

        # Test that referral object is not created
        new_user = User.objects.get(email='test@example.com')
        with self.assertRaises(Referral.DoesNotExist):
            Referral.objects.get(referred=new_user)

    def test_user_registration_with_incorrect_referral_code(self):
        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'buyer',
            'referral_code': 'invalid_code'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

        # Test that referral object is not created
        new_user = User.objects.get(email='test@example.com')
        with self.assertRaises(Referral.DoesNotExist):
            Referral.objects.get(referred=new_user)

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
        