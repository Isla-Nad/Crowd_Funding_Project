from django.db import models
from django.urls import reverse
from categories.models import Category, Tag
from django.utils import timezone
from django.contrib.auth.models import User


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30,)
    details = models.CharField(max_length=30)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='projects')
    total_target = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    cover = models.ImageField(
        upload_to='projects/images/', max_length=200, null=True)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    def get_image_url(self):
        return f'/media/{self.cover}'

    def get_show_url(self):
        url = reverse('View', args=[self.id])
        return url


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='projects/images/', max_length=200, null=True)

    def __str__(self):
        return f"{self.image}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    review_desp = models.CharField(max_length=100)
    rating = models.IntegerField()

    def __str__(self) -> str:
        return self.review_desp


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_date = models.DateTimeField(auto_now_add=True)


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self) -> str:
        return self.project.title


class ReportComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self) -> str:
        return self.review.review_desp
