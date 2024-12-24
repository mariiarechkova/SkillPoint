from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from ..serializers import *
from ..utils import generate_jwt

class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        user_data = {key: value for key, value in request.data.items()}
        serializer = UserSerializer(data=user_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = get_object_or_404(User, email=email)

        pwd_valid = check_password(password, user.password)
        # user = authenticate(email=email, password=password)
        if not pwd_valid:
            raise AuthenticationFailed("Invalid credentials")

        token = generate_jwt(user)
        return Response({"token": token})


class ProtectedView(APIView):
    def get(self, request):
        return Response({"message": "You are authenticated", "user": str(request.user)})