import re
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
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


class EmailAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


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
        fields = ['bio', 'profile_picture',
                  'birthdate', 'facebook_profile', 'country']


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
