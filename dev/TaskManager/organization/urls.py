from django.urls import path
from .views import *

urlpatterns = [

    path('organizations/', OrganizationList.as_view(), name='organization-list'),
    path('organizations/<slug:slug>/', OrganizationDetail.as_view(), name='organization-detail'),

]
