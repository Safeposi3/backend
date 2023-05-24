from api.models import Buoys
from rest_framework import serializers
from api.serializers import ReservationSerializer
class BuoySerializer(serializers.ModelSerializer):
    reservations = serializers.SerializerMethodField()

    class Meta:
        model = Buoys
        fields = ['id', 'name', 'location', 'latitude', 'longitude', 'created_at', 'updated_at', 'reservations']

    def get_reservations(self, obj):
        reservations = obj.get_reservations()
        return ReservationSerializer(reservations, many=True).data