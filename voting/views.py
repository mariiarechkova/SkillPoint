from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *

class VoteEventsView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return get_object_or_404(VoteEvent, pk=pk)

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

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"error": "Details should be a list of objects."}, status=status.HTTP_400_BAD_REQUEST)

class MetricsStaffView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(organisation=self.request.user.organisation)

        for user in users:
            average_rating = VoteDetails.objects.filter(
                rated_user=user).aggregate(
                average=Avg('estimation'))['average'] or 0
            user.average_rating = round(average_rating, 2)

        serializer = MetricsStaffSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MetricsVoteView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(organisation=self.request.user.organisation)
        serializer = MetricsVoteSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
