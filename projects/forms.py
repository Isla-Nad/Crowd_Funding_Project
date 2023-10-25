from projects.models import Report, ReportComment
from django import forms
from categories.models import Category, Tag
from projects.models import Donation, Project, Review
from django.forms import ModelForm
from django.forms.widgets import NumberInput


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProjectForm(ModelForm):
    title = forms.CharField(required=True)
    details = forms.CharField(required=True)
    category = forms.ModelChoiceField(
        Category.objects.all(),
        label="Category"
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
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    images = MultipleFileField()

    class Meta:
        model = Project
        fields = ['title', 'details',  'category', 'total_target',
                  'start_time', 'end_time', 'tags', 'images', ]


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donation_amount']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_desp']


class ProjectReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'description']

#! Report comment 
class CommentReportForm(forms.ModelForm):
    class Meta:
        model = ReportComment
        fields = ['reason', 'description']
