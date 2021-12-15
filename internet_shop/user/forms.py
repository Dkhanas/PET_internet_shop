from django.contrib.auth.forms import UserCreationForm, forms

from .models import User
from utils.constants import EMAIL_FIELD, USERNAME_HELP_TEXT


class SignUpForm(UserCreationForm, forms.Form):
    username = forms.CharField(label='Username', max_length=EMAIL_FIELD, help_text=USERNAME_HELP_TEXT)

    class Meta:
        model = User
        fields = ('password1', 'password2')

    field_order = ['username']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=EMAIL_FIELD)
    password = forms.CharField(label='Password', min_length=8, widget=forms.PasswordInput)
