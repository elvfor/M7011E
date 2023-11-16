
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    #path("TaskManagerApp/", include("TaskManagerApp.urls")),
    path('api/v1/', admin.site.urls),
    path('admin/', include('TaskManagerApp.urls')),
]
