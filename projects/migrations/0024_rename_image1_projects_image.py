# Generated by Django 4.2.6 on 2023-10-20 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0023_remove_projects_image2_remove_projects_image3'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projects',
            old_name='image1',
            new_name='image',
        ),
    ]
