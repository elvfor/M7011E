from django.db import models

# Create your models here.
class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique = True)
    slug = models.SlugField(null = True, unique=True)

    objects = models.Manager()

    #def save(self, *args, **kwargs):
    #    if not self.slug or self.name != self.slug:
    #        self.slug = slugify(self.name)
    #    super().save(*args, **kwargs)

    def __str__(self):
        return self.name

