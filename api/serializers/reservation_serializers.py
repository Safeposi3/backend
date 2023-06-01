from rest_framework import serializers
from api.models import Reservation, Buoys

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'buoy', 'start_time', 'end_time', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user']

    def validate(self, data):
        """
        Check that the start is before the end.
        """
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must occur after start time")
        return data

    def to_representation(self, instance):
        self.fields['buoy'] = BuoysSerializer(read_only=True)
        return super().to_representation(instance)


class BuoysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buoys
        fields = ['id', 'latitude', 'longitude', 'size', 'created_at', 'updated_at', 'reservations', 'price1', 'price2']
        read_only_fields = ['price1', 'price2']

    def to_representation(self, instance):
        self.fields['reservations'] = ReservationSerializer(many=True, read_only=True)
        return super().to_representation(instance)
    
    def create(self, validated_data):
        # Remove the price1 and price2 fields from the validated data
        validated_data.pop('price1', None)
        validated_data.pop('price2', None)
