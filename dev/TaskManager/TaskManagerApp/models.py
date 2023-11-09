from django.contrib.auth.models import User
from django.db import models

from django.db import models

class Organization(models.Model):
    organization_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)  # Add other organization-related details as needed

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    projects = models.ManyToManyField('Project')


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    email = models.EmailField()

class SuperUser(models.Model):
    super_user_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields specific to the SuperUser if needed

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    super_user = models.OneToOneField('SuperUser', on_delete=models.CASCADE)

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    estimated_time = models.DecimalField(max_digits=5, decimal_places=2)
    label = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)