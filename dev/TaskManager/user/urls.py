from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    path('user/create/', CreateUserView.as_view(), name='create'),
    path('user/token/', CreateTokenView.as_view(), name='token'),
    path('user/update', ManageUserView.as_view(), name='update'),
    path('user/delete/', DeleteUserView.as_view(), name='delete'),
    path('user/retrieve/', RetrieveUserView.as_view(), name='retrieve'),
]
