from rest_framework import serializers
from api.models import Buoys
from .reservation_serializers import ReservationSerializer

class BuoysSerializer(serializers.ModelSerializer):
    reservations = ReservationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Buoys
        fields = ['id', 'latitude', 'longitude', 'size', 'created_at', 'updated_at', 'reservations', 'price1', 'price2']
        read_only_fields = ['price1', 'price2']

    def create(self, validated_data):
        # Remove the price1 and price2 fields from the validated data
        validated_data.pop('price1', None)
        validated_data.pop('price2', None)

        return super().create(validated_data)