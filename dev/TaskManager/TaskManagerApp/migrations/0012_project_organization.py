# Generated by Django 4.2.7 on 2023-11-17 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManagerApp', '0011_alter_project_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TaskManagerApp.organization'),
        ),
    ]
