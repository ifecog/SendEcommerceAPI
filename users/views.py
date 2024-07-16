from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated


from .models import User
from .serializers import (
    UserSerializer,
    UserSerializerWithToken,
    SigninSerializer
)

# Create your views here.

class SigninView(TokenObtainPairView):
    serializer_class = SigninSerializer
    

@api_view(['POST'])
def signup(request):
    data = request.data
    
    if User.objects.filter(email=data['email']).exists():
        return Response({'detail': 'User with email already exists!'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(phone_number=data['phone_number']).exists():
        return Response({'detail': 'User with phonenumber already exists!'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.create_user(
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data['email'],
            phone_number=data['phone_number'],
            password=make_password(data['password'])   
        )
        
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        message = {'detail', str(e)}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
