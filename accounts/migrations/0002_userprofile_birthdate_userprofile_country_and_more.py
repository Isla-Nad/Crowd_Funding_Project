# Generated by Django 4.2.6 on 2023-10-19 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='facebook_profile',
            field=models.URLField(blank=True, null=True),
        ),
    ]
