from django.db import models
from django.shortcuts import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(null=True, blank=True)
    image = models.ImageField(upload_to='cat/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    def get_show_url(self):
        url = reverse('View', args=[self.id])
        return url


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
