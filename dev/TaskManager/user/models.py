from django.db import models
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    home_address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
