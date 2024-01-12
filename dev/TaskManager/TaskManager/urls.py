
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import ( SpectacularAPIView, SpectacularSwaggerView
)

from TaskManager import settings

urlpatterns = [
    path(
        '',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('admin/', admin.site.urls),
    #path('api/v1/user/', include('user.urls')),
    path('api/v1/', include('organization.urls')),
    path('api/v1/', include('project.urls')),
    path('api/v1/', include('task.urls')),
    path('api/v1/', include('user.urls')),
    path('main/', include('main.urls')),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        # ... other URL patterns ...
    ]