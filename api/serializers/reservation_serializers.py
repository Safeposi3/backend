from rest_framework import serializers
from api.models import Reservation,Buoys
from api.serializers import ReservationSerializer

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
    
class ReservationSerializer(serializers.ModelSerializer):
    buoy = BuoysSerializer(read_only=True)  # Use BuoysSerializer
    buoy_id = serializers.PrimaryKeyRelatedField(source='buoy', queryset=Buoys.objects.all(), write_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'buoy', 'buoy_id', 'start_time', 'end_time', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user']
    

    def validate(self, data):
        """
        Check that the start is before the end.
        """
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must occur after start time")
        return data