from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordChangeForm
from django.forms import ModelForm
from django import forms
from .models import Advert, User

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

    location = forms.CharField(required=True,label='Location',widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Latitude,Longitude'
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'location')
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

    location = forms.CharField(required=True,label='Location',widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Latitude,Longitude'
        }
    ))

    photo_url = forms. CharField(required=False, label='Photo',widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'URL of your photo'
        }
    ))

    contact = forms.CharField(required=False,label='Contact',widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Phone number'
        }
    ))

    preferences = forms.CharField(required=False,label='Preferences',widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Allergen1, Allergen2, ...'
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'location','photo_url','contact','preferences')
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

class CreateAdvertForm(forms.ModelForm):
    name = forms.CharField(required=True,label='Name',widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Name of your product'
        }
    ))

    description = forms.CharField(required=True,label='Description',widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Description of your product'
        }
    ))

    amount_available = forms.CharField(required=True,label='Amount',widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'step': 1,
            'min': '1',
            'max': '200',
            'value': 1
        }
    ))

    allergens = forms.CharField(required=True,label='Allergens',widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Allergen 1 ; Allergen 2; ...'
        }
    ))

    photo_url = forms.CharField(required=False,label='Photo URL',widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'URL of the photo to describe your product'
        }
    ))

    class Meta:
        model = Advert
        fields = ('name', 'description', 'amount_available', 'allergens', 'photo_url')
        help_texts = {
            'name': '',
            'description': '',
        }