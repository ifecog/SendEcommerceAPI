from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (
    SigninView,
    signup,
)

urlpatterns = [
    path('signin/', SigninView.as_view(), name='user-signin'),
    path('signup/', signup, name='user-signup'),
    
    # Token refresh/verify
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-refresh'),
]