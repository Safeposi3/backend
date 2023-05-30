from knox import views as knox_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ShipViewSet,LoginApi,RegisterApi,UserDetail,ReservationViewSet,BuoyViewSet,AdminShipViewSet,AdminReservationViewSet,AdminUserViewSet,EmailVerificationView,CreatePaymentIntentView

router = DefaultRouter()
router.register(r'ships', ShipViewSet)
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'buoys', BuoyViewSet)
router.register(r'admin/ships', AdminShipViewSet, basename='admin_ships')
router.register(r'admin/reservations', AdminReservationViewSet, basename='admin_reservations')
router.register(r'admin/users', AdminUserViewSet, basename='admin_users')

urlpatterns = [
    path('login/', LoginApi.as_view(), name='login_api'),
    path('register/', RegisterApi.as_view(), name='register_api'),
    path('users/', UserDetail.as_view(), name='user_detail'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout_api'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logout_all_api'),
    path('verify-email/', EmailVerificationView.as_view(), name='verify_email'),
    path('create-payment/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('', include(router.urls)),
]