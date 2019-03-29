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
# @permission_classes((AllowAny, ))
class FlightViewSet(viewsets.ModelViewSet):
    queryset = models.Flight.objects.all()
    serializer_class = serializers.FlightSerializer

    @detail_route(['post', 'put'])
    def reserve(self, request, pk=None):
        """
        This function allows a user to reserve/book a flight
        :param request: request object
        :param pk: flight Id
        :return: response with flight details or error
        """
        book_flag_msg = 'reserved'
        flight = get_object_or_404(models.Flight, pk=pk)
        serializer = serializers.FlightSerializer(flight)
        booking = get_object_or_none(models.Booking, user=request.user, flight=flight)
        if request.method == 'PUT':
            book_flag_msg = 'booked'
            booking.booked = request.data['booked']
        elif request.method == 'POST':
            if booking:
                return Response({
                    'message': 'You have already reserve this flight'
                }, status=status.HTTP_409_CONFLICT)

            booking = models.Booking(flight=flight, user=request.user)

        booking.save()

        return Response({
            'message': 'Flight successfully %s' % book_flag_msg,
            'data': {
                'flight_details': serializer.data,
                'booked': booking.booked
            }
        })
