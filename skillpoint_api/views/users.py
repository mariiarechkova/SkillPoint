from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Profile, User
from ..serializers import UserSerializer, ProfileSerializer


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

            user_data.pop('organisation', None)

            try:
                profile = Profile.objects.get(user=user)
                profile_data = ProfileSerializer(profile).data
            except:
                profile_data = {}

            combined_data = {**user_data, **profile_data}
            return Response(combined_data)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class AvailibleUsers(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)


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
