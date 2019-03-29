from rest_framework import serializers
from . import models


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'no_of_seats': {'write_only': True}
        }

        model = models.Flight
        fields = [
            'id',
            'from_location',
            'to_location',
            'departure_time',
            'arrival_time',
            'price',
            'no_of_seats',
            'passengers',
        ]

    def validate(self, data):
        """
        check that to and from locations are not the same
        :param data:
        :return:
        """
        if data['to_location'] == data['from_location']:
            raise serializers.ValidationError('from and to location cannot be the same')
        return data


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        fields = '__all__'
