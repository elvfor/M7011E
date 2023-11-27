
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    #path("TaskManagerApp/", include("TaskManagerApp.urls")),
    path('admin/', admin.site.urls),
    #path('api/v1/', include('TaskManagerApp.urls')),
    path('api/v1/', include('organization.urls')),
    path('api/v1/', include('project.urls')),
    path('api/v1/', include('task.urls')),
    path('api/v1/', include('user.urls')),
]
