from rest_framework import serializers
from skillpoint_api.models import *

organisation_field = serializers.PrimaryKeyRelatedField(queryset=Organisation.objects.all())

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(source='created_at', format="%Y-%m-%d")
    organisation = organisation_field
    class Meta:
        model = Department
        fields = ['id', 'title', 'organisation', 'created']
        read_only_fields = ['created']

class VoteEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteEvent
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(source='created_at', format="%Y-%m-%d")
    password = serializers.CharField(write_only=True)

    organisation = organisation_field

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