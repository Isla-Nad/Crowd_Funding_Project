from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from accounts.models import UserProfile


class AccountCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, help_text="Required. Enter your first name.")
    last_name = forms.CharField(
        max_length=30, required=True, help_text="Required. Enter your last name.")
    email = forms.EmailField(max_length=254, required=True,
                             help_text="Required. Enter a valid email address")
    mobile_phone = forms.CharField(
        max_length=15, required=True, help_text="Required. Enter your mobile phone number")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', 'mobile_phone')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture',
                  'birthdate', 'facebook_profile', 'country']


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
