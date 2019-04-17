from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Flight

User = get_user_model()


class FlightBookingTestBaseClass(TestCase):
    def setUp(self):
        self.f1 = Flight.objects.create(
            from_location='Imo',
            to_location='Kaduna',
            departure_time='2019-03-25T14:00:00Z',
            arrival_time='2019-03-25T14:45:00Z',
            price=2000,
            no_of_seats=200
        )
        self.valid_data = {
           'from_location': 'Lagos',
           'to_location': 'Katsina',
           'departure_time': '2019-03-25T14:00:00Z',
           'arrival_time': '2019-03-25T14:45:00Z',
           'price': 1000,
           'no_of_seats': 100
        }

        self.same_to_from_data = {
            'from_location': 'Lagos',
            'to_location': 'Lagos',
            'departure_time': '2019-03-25T14:00:00Z',
            'arrival_time': '2019-03-25T14:45:00Z',
            'price': 1000,
            'no_of_seats': 100
        }

        self.invalid_data = {
            'to_location': 'Katsina',
            'departure_time': '2019-03-25T14:00:00Z',
            'arrival_time': '2019-03-25T14:45:00Z',
            'price': 1000,
            'no_of_seats': 100
        }

        self.update_data = {
            'from_location': 'Sokoto',
            'to_location': 'Kaduna',
            'departure_time': '2019-03-25T14:00:00Z',
            'arrival_time': '2019-03-25T14:45:00Z',
            'price': 1000,
            'no_of_seats': 100
        }

        self.user = User.objects.create_user(
            email='testuser@gmail.com',
            username='tester',
            password='samplepassword'
        )

        self.admin = User.objects.create_superuser(
            email='adminuser@gmail.com',
            username='admin',
            password='adminpassword'
        )
        self.client = APIClient()
        self.client.login(email=self.user.email, password='samplepassword')
        self.token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin)
        self.base_url = '/api/v1/'


# Create your tests here.
class FlightViewSetTest(FlightBookingTestBaseClass):

    def test_unauthorized_get_all_flights(self):
        response = self.client.get(f'{self.base_url}flights/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_authorized_get_all_flights(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(f'{self.base_url}flights/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_flight_creation_same_to_from_location(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post(f'{self.base_url}flights/', self.same_to_from_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'from and to location cannot be the same')

    def test_flight_creation_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(f'{self.base_url}flights/', self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')

    def test_flight_creation_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post(f'{self.base_url}flights/', self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])

    def test_flight_creation_with_missing_parameters(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post(f'{self.base_url}flights/', self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['from_location'][0], 'This field is required.')

    def test_unauthorized_flight_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(f'{self.base_url}flights/{self.f1.id}/', self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')

    def test_successful_flight_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.put(f'{self.base_url}flights/{self.f1.id}/', self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.f1.id)

    def test_unauthorized_flight_deletion(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(f'{self.base_url}flights/{self.f1.id}/', self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')

    def test_successful_flight_deletion(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.delete(f'{self.base_url}flights/{self.f1.id}/', self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)


class FlightBookingViewTest(FlightBookingTestBaseClass):
    """

    """
    def test_reserving_flight_that_does_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(f'{self.base_url}flight/100/reserve/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_unauthorised_flight_reservation(self):
        response = self.client.post(f'{self.base_url}flight/{self.f1.id}/reserve/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_successful_flight_reservation(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(f'{self.base_url}flight/{self.f1.id}/reserve/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'flight successfully reserved')
        self.assertEqual(response.data['data']['flight_details']['id'], self.f1.id)
        self.assertEqual(response.data['data']['booking']['booked'], False)

    def test_booking_flight_that_does_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(f'{self.base_url}flight/100/reserve/', {'booked': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_unauthorised_flight_booking(self):
        response = self.client.put(f'{self.base_url}flight/{self.f1.id}/reserve/', {'booked': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_successful_flight_booking(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(f'{self.base_url}flight/{self.f1.id}/reserve/', {'booked': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'flight successfully booked')
        self.assertEqual(response.data['data']['flight_details']['id'], self.f1.id)
        self.assertEqual(response.data['data']['booking']['booked'], True)

    def test_double_reserving_flight(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(f'{self.base_url}flight/{self.f1.id}/reserve/')
        d_response = self.client.post(f'{self.base_url}flight/{self.f1.id}/reserve/')
        self.assertEqual(d_response.data['message'], 'You have already reserve this flight')
        self.assertEqual(d_response.status_code, status.HTTP_409_CONFLICT)
