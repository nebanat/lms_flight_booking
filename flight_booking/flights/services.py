from django.forms.models import model_to_dict
from . import models, serializers
from .helpers.db import get_object_or_none
from .helpers.email import send_email_with_booked_flight_details
from rest_framework.exceptions import APIException

from django.contrib.auth import get_user_model

from users.serializers import UserSerializer

User = get_user_model()


def reserve_flight(requestor, flight):
    """
     reserve a flight
    :param requestor: requestor(logged in user)
    :param flight: flight to be reserved
    :return:
    """
    flight_serializer = serializers.FlightSerializer(flight)
    booking = get_object_or_none(models.Booking, user=requestor, flight=flight)

    if booking:
        raise APIException('You have already reserve this flight')

    booking = models.Booking(flight=flight, user=requestor)
    booking_serializer = serializers.BookingSerializer(
        data=model_to_dict(booking)
    )
    booking_serializer.is_valid(raise_exception=True)
    booking_serializer.save()

    return flight_serializer.data, booking_serializer.data


def book_flight(requestor, flight, data):
    """
    book a flight
    :param requestor: requestor(logged in user)
    :param flight: flight to be reserved
    :param data: request data
    :return:
    """
    flight_serializer = serializers.FlightSerializer(flight)
    booking, created = models.Booking.objects.get_or_create(flight=flight, user=requestor)
    book_status = data.get('booked', None)
    booking_serializer = serializers.BookingSerializer(booking, data=dict(user=requestor.id,
                                                                          flight=flight.id,
                                                                          booked=book_status
                                                                          ))
    booking_serializer.is_valid(raise_exception=True)
    booking_serializer.save()

    send_email_with_booked_flight_details(booking)  # runs on different thread

    return flight_serializer.data, booking_serializer.data


def get_flight_passenger_count(flight):
    """

    :param flight:
    :return:
    """
    flight_serializer = serializers.FlightSerializer(flight)
    passengers_set = User.objects.filter(
        booking__flight=flight.id,
        booking__booked=True
    )
    passengers = UserSerializer(passengers_set, many=True)
    return flight_serializer.data, passengers.data, passengers_set.count()
