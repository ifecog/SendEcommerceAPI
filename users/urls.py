from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (
    LoginView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='user-login'),
]