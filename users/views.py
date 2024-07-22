from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404

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
        user = User.objects.create(
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
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    data = request.data
    serializer = UserSerializerWithToken(user, many=False)
    
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.phone_number = data['phone_number']
    
    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user_by_id(request, uuid):
    user = get_object_or_404(User, uuid=uuid)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_user(request, uuid):
    user = get_object_or_404(User, uuid=uuid)

    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.phone_number = data['phone_number']
    user.is_staff = data['isAdmin']

    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, uuid):
    user = get_object_or_404(User, uuid=uuid)
    user.delete()
    return Response('User Deleted!')