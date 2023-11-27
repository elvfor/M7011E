from django.http import HttpResponse
from .serializers import *
from .models import Task
from rest_framework import generics, viewsets, permissions
from django.shortcuts import get_object_or_404