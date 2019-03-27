from rest_framework import serializers
from . import models


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Flight
        fields = '__all__'

    def validate(self, data):
        """
        check that to and from locations are not the same
        :param data:
        :return:
        """
        if data['to_location'] == data['from_location']:
            raise serializers.ValidationError('from and to location cannot be the same')
        return data

