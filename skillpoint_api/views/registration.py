from django.shortcuts import get_object_or_404
from django.utils.timezone import now
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
        vote_event_id = request.query_params.get('vote_event_id')
        if not vote_event_id:
            return Response(
                {"error": "vote_event_id is required as a query parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )

        vote_event = get_object_or_404(VoteEvent, id=vote_event_id)

        user_data = request.data.copy()
        user_data['created'] = now()
        user_data['organisation'] = vote_event.organisation_id

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