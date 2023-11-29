from django.urls import path
from .views import *

urlpatterns = [

    path('projects/<slug:slug>/tasks/', TaskList.as_view(), name='task-list'),
    path('tasks/<slug:slug>/', TaskDetail.as_view(), name='task-detail'),

]
