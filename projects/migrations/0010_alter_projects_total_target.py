# Generated by Django 4.2.6 on 2023-10-18 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_projects_total_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='total_target',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
