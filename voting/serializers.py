from django.db.models import Sum
from rest_framework import serializers

from organisations.models import Organisation
from organisations.serializers import DepartmentSerializer
from users.models import User
from voting.models import VoteEvent, VoteRoundDetails


class VoteEventSerializer(serializers.ModelSerializer):
    organisation = serializers.PrimaryKeyRelatedField(
        queryset=Organisation.objects.all(),
        write_only=True
    )
    class Meta:
        model = VoteEvent
        fields = ['id','frequency', 'start_day', 'end_day', 'organisation']

class VoteDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteRoundDetails
        fields = '__all__'

class MetricsStaffSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    image = serializers.CharField(source='profile.image', read_only=True)
    scale_interpretation = serializers.CharField(default='<1')
    average_rating = serializers.FloatField()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'image', 'scale_interpretation', 'average_rating', 'department']


class MetricsVoteSerializer(serializers.ModelSerializer):
    evaluation_reports = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'evaluation_reports', 'total']

    def get_evaluation_reports(self, user):
        vote_details = VoteRoundDetails.objects.filter(rated_user=user).select_related('judge')
        return [
            {
                'estimation': vote.estimation,
                'judge_user': {
                    'id': vote.judge.id,
                    'first_name': vote.judge.first_name,
                    'last_name': vote.judge.last_name
                }
            }
            for vote in vote_details
        ]
    def get_total(self,user):
        vote_details = VoteRoundDetails.objects.filter(rated_user=user)
        return round(vote_details.aggregate(total=Sum('estimation'))['total'] or 0, 2)
