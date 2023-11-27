from django.shortcuts import render
from django.http import HttpResponse
from .serializers import *
from .models import Organization
from rest_framework import generics, viewsets, permissions
from django.shortcuts import get_object_or_404
# Create your views here.
class OrganizationList(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class OrganizationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = 'slug'
