from rest_framework import viewsets, permissions
from api.serializers import BuoysSerializer
from api.models import Buoys
from rest_framework.permissions import IsAuthenticated, AllowAny


class BuoyViewSet(viewsets.ModelViewSet):
    queryset = Buoys.objects.all()
    serializer_class = BuoysSerializer
    permission_classes = [AllowAny]