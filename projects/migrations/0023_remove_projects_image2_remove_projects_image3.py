# Generated by Django 4.2.6 on 2023-10-20 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_projects_image3'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='projects',
            name='image3',
        ),
    ]
