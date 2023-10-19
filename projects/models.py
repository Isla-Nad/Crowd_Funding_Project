from django.db import models
from django.shortcuts import reverse
from categories.models import Category
from django.utils import timezone 

class Projects(models.Model):
    title= models.CharField(max_length=30,)
    details= models.CharField(max_length=30)
    image=models.ImageField(upload_to='projects/images/',max_length=200 ,null=True)
    cat=models.ForeignKey(Category, on_delete=models.CASCADE,null=True ,blank=True)  
    total_target = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    created_at= models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.title}" 

    def get_image_url(self):
        return f'/media/{self.image}'
    def get_show_url(self):
        url = reverse('View', args=[self.id])
        return url
# class Image(models.Model):
#     images = models.ImageField(upload_to="projects/images/")
#     project = models.ForeignKey(Projects, on_delete=models.CASCADE, default=None)  

