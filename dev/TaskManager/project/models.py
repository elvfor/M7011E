from django.db import models
from django.contrib.auth.models import User
from organization.models import Organization

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null = True)
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return self.name
