from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework import viewsets
from . import models, serializers
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, detail_route
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
# @permission_classes((AllowAny, ))
class FlightViewSet(viewsets.ModelViewSet):
    queryset = models.Flight.objects.all()
    serializer_class = serializers.FlightSerializer

    @detail_route(['post', 'put'])
    def reserve(self, request, pk=None):
        booking = None
        book_flag_msg = 'reserved'
        flight = get_object_or_404(models.Flight, pk=pk)
        serializer = serializers.FlightSerializer(flight)
        if request.method == 'PUT':
            booking = models.Booking.objects.get(user=request.user, flight=flight)
            book_flag_msg = 'booked'
            booking.booked = request.data['booked']
        elif request.method == 'POST':
            booking = models.Booking(flight=flight,
                                     user=request.user)

        try:
            booking.save()
        except IntegrityError:
            return Response({
                'message': 'You have already %s this flight' % book_flag_msg
            }, status=status.HTTP_409_CONFLICT)

        return Response({
            'message': 'Flight successfully %s' % book_flag_msg,
            'data': {
                'flight_details': serializer.data,
                'booked': booking.booked
            }
        })
