from django import forms
from datetime import datetime
from categories.models import Category

from django.forms.widgets import NumberInput

class Projectsform(forms.Form):
    title=forms.CharField(required=True)
    details =forms.CharField(required=True)
    image=forms.ImageField()
    cat=forms.ModelChoiceField(
        Category.objects.all(),label="Category"
    )
    total_target = forms.DecimalField()
    start_time = forms.DateTimeField(
        widget=NumberInput(
            attrs={
                'placeholder': 'Start date & time',
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ))

    end_time = forms.DateTimeField(
        widget=NumberInput(
            attrs={
                'placeholder': 'End date & time',
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ))
  

    