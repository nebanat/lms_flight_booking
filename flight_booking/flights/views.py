from django.shortcuts import render
from rest_framework import viewsets
from . import models, serializers


# Create your views here.
class FlightViewSet(viewsets.ModelViewSet):
    queryset = models.Flight.objects.all()
    serializer_class = serializers.FlightSerializer
