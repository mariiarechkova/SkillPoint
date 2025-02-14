from rest_framework import serializers
from organisations.models import Organisation
from users.models import User, Profile, Role


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    organisation = serializers.PrimaryKeyRelatedField(
        queryset=Organisation.objects.all(),
        write_only=True
    )

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'organisation', 'password', 'department', 'is_staff']
        read_only_fields = ['vote_events']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image', 'job_title', 'description', 'salary', 'start_work_at']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'title', 'weight_vote']

    def validate_weight_vote(self, value):
        """check that the value is within acceptable limits."""
        if not (1.0 <= value <= 10.0):
            raise serializers.ValidationError("The score should be from 1.0 to 10.0")
        return value