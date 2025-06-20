from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginUser

urlpatterns = [
    path(
        'login-user/',
        LoginUser.as_view(),
        name='login'
    ),
    
    path(
        'logout-user/',
        LogoutView.as_view(),
        name='logout'
    ),
]
