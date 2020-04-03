from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Image, Profile, Comment

class FormSignUp(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required. Kindly use a valid email address')

class Meta:
    model = User
    fields = ('username','password1','password2','email')

class FormLogin(forms.ModelForm):
    username = forms.CharField(label='Username',max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User 
        fields = ('username', 'password')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exlcude = ['follower_user', 'following_user']
        fields = ('about', 'profile_picture')
        
class FormImage(forms.ModelForm):
    class Meta:
        model = Image
        exclude = []
        fields = ('image_name', 'image_caption', 'image','profile')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['image_id', 'user_id']
        fields = ('comment',)