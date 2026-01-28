from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_api(request):
    data = request.data
    if data['password'] != data['confirm_password']:
        return Response({"error": "passwords do not match"}, status=400)

    if User.objects.filter(username=data['username']).exists():
        return Response({"error": "username exists"}, status=400)

    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        first_name=data['full_name']
    )

    return Response({"message": "account created"}, status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    user = authenticate(
        username=request.data.get("username"),
        password=request.data.get("password")
    )

    if not user:
        return Response({"error": "invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "is_admin": user.is_superuser
    })
