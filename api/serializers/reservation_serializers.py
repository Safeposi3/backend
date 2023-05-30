from rest_framework import serializers
from api.models import Reservation,Buoys

class ReservationSerializer(serializers.ModelSerializer):
    buoy = serializers.SlugRelatedField(slug_field='id', queryset=Buoys.objects.all())
    
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