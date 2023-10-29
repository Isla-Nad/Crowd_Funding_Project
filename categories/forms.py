from django import forms
from categories.models import Category, Tag
from projects.models import Donation,Report


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'
        
        
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'