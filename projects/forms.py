from django import forms
from categories.models import Category
from projects.models import Projects
from django.forms import ModelForm
from django.forms.widgets import NumberInput
# from projects.models import Tag


class Projectsform(ModelForm):
    title = forms.CharField(required=True)
    details = forms.CharField(required=True)
    # image = forms.ImageField()
    cat = forms.ModelChoiceField(
        Category.objects.all(), label="Category"
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
    # tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
    #                                         widget=forms.SelectMultiple(
    #     attrs={
    #         "class": "form-control"
    #     }
    # ),required=False)
    class Meta:
            model=Projects
            fields='__all__'
class Dontate(ModelForm):
       total_target = forms.DecimalField()
       class Meta:
            model=Projects
            fields= ('total_target',)
                  
