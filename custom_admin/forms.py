import re
from django import forms
from accounts.models import UserProfile
from categories.models import Category, Tag
from projects.models import Donation, Report, ReportComment, Review
from django.contrib.auth.forms import UserCreationForm, UserChangeForm as BaseUserChangeForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True,
                             help_text="Required. Enter a valid email address")

    class Meta:
        model = User
        fields = ('username', 'email',
                  'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        if not re.match(r'^01[0-2]\d{8}$', mobile_phone):
            raise forms.ValidationError(
                "Enter a valid Egyptian mobile phone number.")
        return mobile_phone


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'is_active', 'is_staff', 'is_superuser', 'password']


class UserProfileForm(forms.ModelForm):
    birthdate = forms.DateTimeField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'birthdate',
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ))

    class Meta:
        model = UserProfile
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'


class ReportCommentForm(forms.ModelForm):
    class Meta:
        model = ReportComment
        fields = '__all__'
