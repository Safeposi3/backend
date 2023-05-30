from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from api.models import Reservation,Buoys
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
        buoy_id = request.data.get('buoy')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        if not buoy_id or not start_time or not end_time:
            return Response("Invalid request. Please provide buoy, start_time, and end_time.", status=status.HTTP_400_BAD_REQUEST)

        try:
            buoy = Buoys.objects.get(id=buoy_id)
        except Buoys.DoesNotExist:
            return Response("Invalid buoy ID.", status=status.HTTP_400_BAD_REQUEST)

        overlapping_reservations = Reservation.objects.filter(
            buoy=buoy,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        for reservation in overlapping_reservations:
            if reservation.status != 'CANCELLED':
                return Response("This buoy has already been booked for the specified time.", status=status.HTTP_400_BAD_REQUEST)


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(buoy=buoy, user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)
    
class AdminReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAdminUser]
