from django.utils.timezone import now
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, AuthenticationFailed
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from .serializers import *
from .utils import generate_jwt


class DepartmentListCreate(APIView):
    def get(self, request, *args, **kwargs):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        department_data = {
            'title': request.data.get("title"),
            'organisation': 1,
            'created': now()
        }
        serializer = DepartmentSerializer(data=department_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        user_data = {key: value for key, value in request.data.items()}
        user_data['organisation'] = 1
        user_data['created'] = now()

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

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

        pwd_valid = check_password(password, user.password)
        # user = authenticate(email=email, password=password)
        if not pwd_valid:
            raise AuthenticationFailed("Invalid credentials")

        token = generate_jwt(user)
        return Response({"token": token})

class ProtectedView(APIView):
    def get(self, request):
        return Response({"message": "You are authenticated", "user": str(request.user)})