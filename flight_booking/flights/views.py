from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from . import models, serializers, services as flight_services
# from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .permissions import IsSuperUserOrReadOnly


# Create your views here.
class FlightViewSet(viewsets.ModelViewSet):
    """
        Flight model viewset
    """
    queryset = models.Flight.objects.all()
    serializer_class = serializers.FlightSerializer
    permission_classes = [IsSuperUserOrReadOnly]  # only admin can create, edit, delete a flight


class FlightBookingView(APIView):
    def post(self, request, flight_pk=None):
        """
        This allows a logged in user reserve a flight
        :param request: request object
        :param flight_pk: flight id
        :return:
        """
        flight = get_object_or_404(models.Flight, pk=flight_pk)
        flight_details, booking_details = flight_services.reserve_flight(request.user, flight)

        return Response({
            'message': 'flight successfully reserved',
            'data': {
                'flight_details': flight_details,
                'booking': booking_details
            }
        }, status=status.HTTP_201_CREATED)

    def put(self, request, flight_pk=None):
        """
        This allows a logged in user reserve/book a flight
        :param request: request object
        :param flight_pk: flight primary key
        :return:
        """
        flight = get_object_or_404(models.Flight, pk=flight_pk)
        flight_details, booking_details = flight_services.book_flight(
            request.user,
            flight,
            request.data)

        return Response({
            'message': 'flight successfully booked',
            'data': {
                'flight_details': flight_details,
                'booking': booking_details
            }
        }, status=status.HTTP_200_OK)
