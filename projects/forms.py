from django import forms
from datetime import datetime
from categories.models import Category


class Projectsform(forms.Form):
    title = forms.CharField(required=True)
    details = forms.CharField(required=True)
    image = forms.ImageField()
    cat = forms.ModelChoiceField(
        Category.objects.all(), label="Category"
    )
    total_target = forms.DecimalField()
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()
