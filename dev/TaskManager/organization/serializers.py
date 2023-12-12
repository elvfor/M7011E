from django.contrib.auth.models import User, Group
from .models import Organization
from rest_framework import serializers
from django.urls import reverse


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug', 'users']
