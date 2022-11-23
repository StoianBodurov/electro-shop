from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from electroshop.accounts.models import Profile

UserModel = get_user_model()


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Email'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input',
            'placeholder': 'Password'
        }))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input',
            'placeholder': 'Repeat Password'
        }))

    class Meta:
        model = UserModel
        fields = ['email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input',
            'placeholder': 'Password'
        }))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'address', 'city', 'zip_code', 'telephone', 'country']


class EditProfileForm(ProfileForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'input',
                    'placeholder': 'Firs Name'
                }),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'input',
                    'placeholder': 'Last Name'
                }),
            'address': forms.TextInput(
                attrs={
                    'class': 'input',
                    'placeholder': 'Address'
                }),
            'city': forms.TextInput(
                attrs={
                    'class': 'input',
                    'placeholder': 'City'
                }),
            'zip_code': forms.TextInput(
                attrs={
                    'class': 'input',
                    'placeholder': 'Zip Code'
                }),
            'telephone': forms.TextInput(
                attrs={
                    'class': 'input',
                    'placeholder': 'Telephone'
                }),
            'country': forms.TextInput(
                attrs={
                    'class': 'input',
                    'placeholder': 'Country'
                }),
        }

