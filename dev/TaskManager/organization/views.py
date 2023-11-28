from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.permissions import IsAdminUser

from .serializers import *
from .models import Organization
from rest_framework import generics, viewsets, authentication, permissions
from django.shortcuts import get_object_or_404

#from .. import organization


class IsPartOfOrg(permissions.BasePermission):
    message = {'detail': 'You must be in this organization to do this.'}

    def has_permission(self, request, view):
        organization_slug = view.kwargs['slug']

        try:
            organization = Organization.objects.get(slug=organization_slug)
        except Organization.DoesNotExist:
            return False

        return request.user in organization.users.all()
class IsOrgLeader(permissions.BasePermission):
    message = {'detail': 'You must be an organization leader to do this.'}

    def has_permission(self, request, view):
        group_name = "Organization Leader"
        return request.user.groups.filter(name=group_name).exists()


class OrganizationList(generics.ListCreateAPIView):
    #queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsOrgLeader | IsAdminUser )]

    def get_queryset(self):
        user = self.request.user
        return Organization.objects.filter(users=user)

class OrganizationDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOrgLeader, IsPartOfOrg]

    serializer_class = OrganizationSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user

        return Organization.objects.filter(users=user)