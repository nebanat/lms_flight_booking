from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from . import models, serializers
from .helpers import get_object_or_none
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, detail_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


# Create your views here.
@permission_classes((AllowAny, ))
class FlightViewSet(viewsets.ModelViewSet):
    queryset = models.Flight.objects.all()
    serializer_class = serializers.FlightSerializer


class FlightBookingView(APIView):
    def post(self, request, format=None, flight_pk=None):
        """
        This allows a logged in user book a flight
        :param request: request object
        :param format:
        :param flight_pk: flight id
        :return:
        """
        flight = get_object_or_404(models.Flight, pk=flight_pk)
        serializer = serializers.FlightSerializer(flight)
        booking = get_object_or_none(models.Booking, user=request.user, flight=flight)

        if booking:
            return Response({
                'message': 'You have already reserve this flight'
            }, status=status.HTTP_409_CONFLICT)

        booking = models.Booking(flight=flight, user=request.user)
        booking.save()

        return Response({
            'message': 'flight successfully reserved',
            'data': {
                'flight_details': serializer.data,
                'booked': booking.booked
            }
        }, status=status.HTTP_201_CREATED)

    def put(self, request, format=None, flight_pk=None):
        """

        :param request:
        :param format:
        :param flight_pk:
        :return:
        """
        flight = get_object_or_404(models.Flight, pk=flight_pk)
        serializer = serializers.FlightSerializer(flight)
        booking, created = models.Booking.objects.get_or_create(flight=flight, user=request.user)
        booking.booked = request.data.get('booked', True)
        return Response({
            'message': 'flight successfully booked',
            'data': {
                'flight_details': serializer.data,
                'booked': booking.booked
            }
        }, status=status.HTTP_201_CREATED)
