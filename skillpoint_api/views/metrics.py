from django.db.models import Avg
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from skillpoint_api.models import User, VoteDetails
from skillpoint_api.serializers import MetricsSerializer


class MetricsView(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.filter(organisation=self.request.user.organisation)

        for user in users:
            average_rating = VoteDetails.objects.filter(
                rated_user=user).aggregate(
                average=Avg('estimation'))['average'] or 0
            user.average_rating = round(average_rating, 2)

        serializer = MetricsSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)