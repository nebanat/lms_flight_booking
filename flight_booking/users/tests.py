from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


# Create your tests here.
class UserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_url = '/api/v1/users'

        self.data_without_email = {
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

        self.data_without_password = {
            'email': 'testuser@gmail.com',
            'password2': 'testpassword',
        }
        self.data_password_repeat_password_no_match = {
            'email': 'testuser@gmail.com',
            'password1': 'testpasswordadd',
            'password2': 'testpassword',
        }
        self.valid_data = {
            'email': 'testuser@gmail.com',
            'password1': 'testpassword234',
            'password2': 'testpassword234',
        }

        self.user = User.objects.create_user(
            email='laurel@gmail.com',
            username='tester',
            password='laurelsamplepassword'
        )

    def test_unsuccessful_sign_up_without_email(self):
        response = self.client.post(f'{self.base_url}/register/',self.data_without_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'This field is required.')

    def test_unsuccessful_sign_up_without_password(self):
        response = self.client.post(f'{self.base_url}/register/', self.data_without_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password1'][0], 'This field is required.')

    def test_password_does_not_match_repeat_password(self):
        response = self.client.post(f'{self.base_url}/register/', self.data_password_repeat_password_no_match,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'The two password fields didn\'t match.')

    def test_successful_signup(self):
        response = self.client.post(f'{self.base_url}/register/', self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['key'])

    def test_login_where_email_does_not_match_record(self):
        response = self.client.post(f'{self.base_url}/login/', {
            'email': 'lofty@gmail.com',
            'password': 'laurelsamplepassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'Unable to log in with provided credentials.')

    def test_login_where_password_does_not_match_record(self):
        response = self.client.post(f'{self.base_url}/login/', {
            'email': 'laurel@gmail.com',
            'password': 'laureljargonpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'Unable to log in with provided credentials.')

    def test_successful_login_with_email_password(self):
        response = self.client.post(f'{self.base_url}/login/', {
            'email': 'laurel@gmail.com',
            'password': 'laurelsamplepassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['key'])



