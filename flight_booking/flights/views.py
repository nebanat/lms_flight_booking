from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from . import models, serializers, services as flight_services
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .permissions import IsSuperUserOrReadOnly


def index(request):
    return render(request, 'flights/home.html')


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


class FlightPassengers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, flight_pk=None):
        flight = get_object_or_404(models.Flight, pk=flight_pk)
        flight_details, passengers, passengers_count = flight_services.get_flight_passenger_count(flight)

        return Response({
            'data': {
                'total_no_of_passengers': passengers_count,
                'flight_details': flight_details,
                'passengers': passengers
            }
        })

