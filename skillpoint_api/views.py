from django.utils.timezone import now
from rest_framework import filters
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

        for department in serializer.data:
            if 'organisation' in department:
                del department['organisation']
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        department_data = {
            'title': request.data.get("title"),
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
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']


class UserDetailView(APIView):

    def get(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(pk=pk)
            user_data = UserSerializer(user).data

            for user in user_data:
                if 'organisation' in user:
                    del user['organisation']

            try:
                profile = Profile.objects.get(user=user)
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
        user_data = {key: value for key, value in request.data.items()}
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


class AvailibleUsers(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        current_user = self.request.user
        return User.objects.exclude(id=current_user.id)


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


class VoteEventsView(APIView):
    def get_object(self, pk):
        try:
            return VoteEvent.objects.get(pk=pk)
        except VoteEvent.DoesNotExist:
            raise NotFound('Vote event not found')

    def get(self, request, pk=None, format=None):
        if pk:
            vote_event = self.get_object(pk)
            serializer = VoteEventSerializer(vote_event)
            return Response(serializer.data)
        else:
            vote_events = VoteEvent.objects.all()
            serializer = VoteEventSerializer(vote_events, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        current_user = self.request.user
        user_data = {key: value for key, value in request.data.items()}
        user_data['organisation'] = current_user.organisation_id

        serializer = VoteEventSerializer(data=user_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        vote_event = self.get_object(pk)
        serializer = VoteEventSerializer(vote_event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        vote_event = self.get_object(pk)
        serializer = VoteEventSerializer(vote_event,
                                    data=request.data,
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vote_event = self.get_object(pk)
        vote_event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VoteDetailsView(APIView):
    def post(self, request, pk, format=None):
        current_user = self.request.user
        vote_details_data = request.data

        if isinstance(vote_details_data, list):
            for detail in vote_details_data:
                detail['judge'] = current_user.id
                detail['vote_event'] = pk

            serializer = VoteDetailsSerializer(data=vote_details_data, many=True)

        else:
            return Response({"error": "Details should be a list of objects."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)