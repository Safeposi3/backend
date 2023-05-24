from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from api.models import Reservation
from api.serializers import ReservationSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        buoy = request.data['buoy']
        start_time = request.data['start_time']
        end_time = request.data['end_time']

        overlapping_reservations = Reservation.objects.filter(buoy=buoy).filter(
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if overlapping_reservations.exists():
            return Response("This buoy has already been booked for the specified time.", status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)