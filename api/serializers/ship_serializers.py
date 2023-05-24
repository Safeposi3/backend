from api.models import Ship
from rest_framework import serializers

class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = '__all__'
    
