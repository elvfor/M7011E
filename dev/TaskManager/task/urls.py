from django.urls import path
from .views import *

urlpatterns = [

    path('projects/<slug:project>/tasks/', TaskList.as_view(), name='task-list'),
    #path('tasks/<slug:slug>/', TaskDetail.as_view(), name='task-detail'),
    path('tasks/<slug:slug>/', views.TaskDetail.as_view(), name='task-detail'),

]
