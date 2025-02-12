from rest_framework import generics, filters
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile, User
from .serializers import UserSerializer, ProfileSerializer
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from .utils import generate_jwt
from voting.models import VoteEvent

class UserList(generics.ListAPIView):
    permission_classes = [IsAdminUser]

    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        current_org = self.request.user.organisation

        return User.objects.filter(organisation=current_org)


class UserDetailView(APIView):

    def get(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(pk=pk)
            user_data = UserSerializer(user).data

            try:
                profile = Profile.objects.get(user=user)
                profile_data = ProfileSerializer(profile).data
            except:
                profile_data = {}

            combined_data = {**user_data, **profile_data}
            return Response(combined_data)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class ProfileView(APIView):

    def get(self, request,  *args, **kwargs):
        try:
            current_user = self.request.user
            user_data = UserSerializer(current_user).data

            try:
                profile = Profile.objects.get(user=current_user)
                profile_data = ProfileSerializer(profile).data
            except:
                profile_data = {}

            combined_data = {**user_data, **profile_data}
            return Response(combined_data)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

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