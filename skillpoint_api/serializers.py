from rest_framework import serializers
from skillpoint_api.models import *


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(source='created_at', format="%Y-%m-%d")

    class Meta:
        model = Department
        fields = ['id', 'title', 'organisation', 'created']
        read_only_fields = ['created']

class VoteEventSerializer(serializers.ModelSerializer):
    organisation = serializers.PrimaryKeyRelatedField(
        queryset=Organisation.objects.all(),
        write_only=True
    )
    class Meta:
        model = VoteEvent
        fields = ['frequency', 'start_day', 'end_day', 'created_at', 'organisation']

class UserSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(source='created_at', format="%Y-%m-%d")
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'organisation', 'password', 'department', 'created']
        read_only_fields = ['vote_events', 'created']

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