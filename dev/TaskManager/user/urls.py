from django.urls import path
from .views import *

app_name = 'user'

#urlpatterns = [
#    path('users/', UserList.as_view(), name='user-list'),
#    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
#
#    path('groups/', GroupList.as_view(), name='group-list'),
#    path('groups/<int:pk>/', GroupDetail.as_view(), name='group-detail'),
#
#]

urlpatterns = [
    path('user/create/', CreateUserView.as_view(), name='create'),
    path('user/token/', CreateTokenView.as_view(), name='token'),
    path('user/update/', ManageUserView.as_view(), name='update'),
]

#"token": "cbba6e3ca718069d2407168eecd2ffb6597e36c3"