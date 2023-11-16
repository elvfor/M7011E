import slug
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.db import models


class Organization(models.Model):
    organization_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique = True)
    slug = models.SlugField(null = True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.name != self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("organization-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)
    slug = models.SlugField(null = True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.project_name)
        super().save(*args, **kwargs)

    #def get_absolute_url(self):
        #return reverse("project_detail", kwargs={"slug": self.slug})


    def __str__(self):
        return self.project_name


class Task(models.Model):

    task_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    estimated_time = models.DecimalField(max_digits=5, decimal_places=2)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('Backlog', 'Backlog'),
        ('Under Progress', 'Under Progress'),
        ('In Review', 'In Review'),
        ('Finished', 'Finished'),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)

    LABEL_CHOICES = [
        ('blocked', 'Blocked'),
        ('bug', 'Bug'),
        ('content', 'Content'),
        ('design', 'Design'),
        ('dev', 'Development'),
        ('enhancement', 'Enhancement'),
        ('product', 'Product'),
    ]
    label = models.CharField(max_length=255, choices=LABEL_CHOICES)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name
