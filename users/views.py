from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django.contrib.auth import get_user_model as User

from .serializers import (
    UserSerializer,
    UserSerializerWithToken,
    LoginSerializer
)

# Create your views here.

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer