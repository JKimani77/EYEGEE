from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Image

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required. Kindly use a valid email address')

class Meta:
    model = User
    fields = ('username','password1','password2','email')

