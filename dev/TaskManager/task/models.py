from django.db import models

class Task(models.Model):

    id = models.AutoField(primary_key=True)
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
    slug = models.SlugField(null=True, unique=True)

    #def save(self, *args, **kwargs):
    #    if not self.slug or self.name != self.slug:
    #        self.slug = slugify(self.name)
    #    super().save(*args, **kwargs)

    def __str__(self):
        return self.name
