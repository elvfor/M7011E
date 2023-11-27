from django.urls import path
from .views import *

urlpatterns = [

    path('organizations/<slug:organization>/projects/', ProjectList.as_view(), name='project-list'),
    path('projects/<slug:slug>/', ProjectDetail.as_view(), name='project-detail'),

]
