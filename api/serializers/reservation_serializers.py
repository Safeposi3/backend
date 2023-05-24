from rest_framework import serializers
from api.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):
        """
        Check that the start is before the end.
        """
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must occur after start time")
        return data