from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique = True)
    slug = models.SlugField(null = True, unique=True)
    users = models.ManyToManyField(User)
    objects = models.Manager()

    def __str__(self):
        return self.name

