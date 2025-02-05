from rest_framework import serializers
from .models import *

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
