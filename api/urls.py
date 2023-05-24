from knox import views as knox_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ShipViewSet,LoginApi,RegisterApi,UserDetail,ReservationViewSet,BuoyViewSet

router = DefaultRouter()
router.register(r'ships', ShipViewSet)
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'buoys', BuoyViewSet)
urlpatterns = [
    path('login/', LoginApi.as_view(), name='login_api'),
    path('register/', RegisterApi.as_view(), name='register_api'),
    path('users/', UserDetail.as_view(), name='user_detail'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout_api'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logout_all_api'),
    path('', include(router.urls)),
]