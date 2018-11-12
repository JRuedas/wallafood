from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordChangeForm
from django.forms import ModelForm
from django import forms

class CreateUserForm(UserCreationForm):
    username = forms.CharField(required=True,label='Username',widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))

    email = forms.CharField(required=True,label='Email',widget=forms.EmailInput(
        attrs={
            'class': 'form-control'
        }
    ))

    password1 = forms.CharField(required=True,label='Password',widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ))

    password2 = forms.CharField(required=True,label='Confirm password',widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': '',
            'password2': '',
        }

class EditProfileForm(UserChangeForm):
    username = forms.CharField(required=True,label='Username',widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))

    first_name = forms.CharField(required=False,label='First name',widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    
    last_name = forms.CharField(required=False,label='Last name',widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))

    email = forms.CharField(required=True,label='Email',widget=forms.EmailInput(
        attrs={
            'class': 'form-control'
        }
    ))

    password = forms.CharField(label='Password',widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'hidden'
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        help_texts = {
            'username': ''
        }

class EditPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(required=True,label='Old password',widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ))
    new_password1 = forms.CharField(required=True,label='New password',widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ))
    new_password2 = forms.CharField(required=True,label='Confirm new password',widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ))
    class Meta:
        model = User