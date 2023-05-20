from django.urls import path
from knox import views as knox_views
from . import views

urlpatterns = [
    path('login/', views.login_api, name='login_api'),
    path('user/', views.get_user_data, name='get_user_data'),
    path('register/', views.register_api, name='register_api'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout_api'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logout_all_api'),
]