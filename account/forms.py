from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    """
    Form for registration
    """

    class Meta:
        model = User
        fields = ('email', 'password')
        labels  = {
            'email': 'E-mail',
            'password': 'Password',
        }

class UserLoginForm(forms.ModelForm):
    """
    Form for login on site
    """

    class Meta:
        model = User
        fields = ('email', 'password')
        labels  = {
            'email': 'E-mail',
            'password': 'Password',
        }
