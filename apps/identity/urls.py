from django.urls import path
from .endpoints import UserRegisterView
from identity.views import (
    CustomTokenObtainView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("jwt/create", CustomTokenObtainView.as_view(), name="token_obtain_pair"),
    path("jwt/refresh", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify", CustomTokenVerifyView.as_view(), name="token_verify"),
]
