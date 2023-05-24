from rest_framework import viewsets, permissions

from rest_framework.permissions import IsAuthenticated
from api.models import Ship
from api.serializers import ShipSerializer
from django.shortcuts import get_object_or_404
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the ship.
        return obj.owner == request.user

class ShipViewSet(viewsets.ModelViewSet):
    queryset = Ship.objects.all()
    serializer_class = ShipSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


    def get_object(self):
        obj = get_object_or_404(self.queryset, owner=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj