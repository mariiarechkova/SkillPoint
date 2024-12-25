from rest_framework import serializers
from skillpoint_api.models import *


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['id', 'name']

class DepartmentSerializer(serializers.ModelSerializer):
    organisation = serializers.PrimaryKeyRelatedField(
        queryset=Organisation.objects.all(),
        write_only=True
    )
    class Meta:
        model = Department
        fields = ['id', 'title', 'organisation']

class VoteEventSerializer(serializers.ModelSerializer):
    organisation = serializers.PrimaryKeyRelatedField(
        queryset=Organisation.objects.all(),
        write_only=True
    )
    class Meta:
        model = VoteEvent
        fields = ['frequency', 'start_day', 'end_day', 'organisation']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    organisation = serializers.PrimaryKeyRelatedField(
        queryset=Organisation.objects.all(),
        write_only=True
    )

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'organisation', 'password', 'department']
        read_only_fields = ['vote_events']

    def create(self, validated_data):
        print(self)
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class VoteDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteDetails
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image', 'job_title', 'description', 'salary', 'start_work_at']


class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class MetricsSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    image = serializers.CharField(source='profile.image', read_only=True)
    scale_interpretation = serializers.CharField(default='<1')
    average_rating = serializers.FloatField()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'image', 'scale_interpretation', 'average_rating', 'department']