from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from rest_framework import viewsets
from . import models, serializers
from .helpers.email import send_email_with_booked_flight_details
from .helpers.db import get_object_or_none
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


# Create your views here.
@permission_classes((AllowAny, ))
class FlightViewSet(viewsets.ModelViewSet):
    queryset = models.Flight.objects.all()
    serializer_class = serializers.FlightSerializer


class FlightBookingView(APIView):
    def post(self, request, flight_pk=None):
        """
        This allows a logged in user book a flight
        :param request: request object
        :param flight_pk: flight id
        :return:
        """
        flight = get_object_or_404(models.Flight, pk=flight_pk)
        flight_serializer = serializers.FlightSerializer(flight)
        booking = get_object_or_none(models.Booking, user=request.user, flight=flight)

        if booking:
            return Response({
                'message': 'You have already reserve this flight'
            }, status=status.HTTP_409_CONFLICT)

        booking = models.Booking(flight=flight, user=request.user)
        booking_serializer = serializers.BookingSerializer(
            data=model_to_dict(booking)
        )
        booking_serializer.is_valid(raise_exception=True)
        booking_serializer.save()

        return Response({
            'message': 'flight successfully reserved',
            'data': {
                'flight_details': flight_serializer.data,
                'booking': booking_serializer.data
            }
        }, status=status.HTTP_201_CREATED)

    def put(self, request, flight_pk=None):
        """

        :param request:
        :param flight_pk:
        :return:
        """
        flight = get_object_or_404(models.Flight, pk=flight_pk)
        serializer = serializers.FlightSerializer(flight)
        booking, created = models.Booking.objects.get_or_create(flight=flight, user=request.user)
        booking.booked = request.data.get('booked', True)
        booking.save()

        send_email_with_booked_flight_details(booking)  # runs on different thread

        return Response({
            'message': 'flight successfully booked',
            'data': {
                'flight_details': serializer.data,
                'booking': booking.booked
            }
        }, status=status.HTTP_200_OK)
