from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(null=True, unique=True)
    password =models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username}"
