# Generated by Django 4.2.7 on 2023-11-16 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManagerApp', '0009_organization_slug_project_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
