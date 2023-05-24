from rest_framework import viewsets, permissions
from api.serializers import BuoySerializer
from api.models import Buoys
from rest_framework.permissions import IsAuthenticated


class BuoyViewSet(viewsets.ModelViewSet):
    queryset = Buoys.objects.all()
    serializer_class = BuoySerializer
    permission_classes = [IsAuthenticated]