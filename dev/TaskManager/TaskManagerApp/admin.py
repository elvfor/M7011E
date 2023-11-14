from django.contrib import admin

# Register your models here.
from .models import Organization, Task, Project, UserProfile

admin.site.register(Organization)
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(UserProfile)

