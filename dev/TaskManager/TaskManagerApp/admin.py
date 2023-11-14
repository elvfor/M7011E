from django.contrib import admin

# Register your models here.
from .models import Organization, Task, Project

admin.site.register(Organization)
admin.site.register(Task)
admin.site.register(Project)
