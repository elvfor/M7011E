from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

#from dev.TaskManager.organization.models import Organization

from organization.models import Organization  # Import the Organization model

# Create your models here.
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null = True)
    slug = models.SlugField(null=True, unique=True)
    #def save(self, *args, **kwargs):
    #    if not self.slug or self.project_name != self.slug:
    #        self.slug = slugify(self.project_name)
    #    super().save(*args, **kwargs)

    def __str__(self):
        return self.name
