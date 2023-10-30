from django import forms
# from categories.models import Category, Tag
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
