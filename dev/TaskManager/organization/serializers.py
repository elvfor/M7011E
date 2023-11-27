from django.contrib.auth.models import User, Group
from .models import Organization
from rest_framework import serializers
from django.urls import reverse
class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug']
