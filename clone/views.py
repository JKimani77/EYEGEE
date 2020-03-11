from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout 
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode #encypt token to base64
from django.utils.encoding import force_bytes, force_text

from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Image, Profile, Comment
from .forms import FormSignUp, FormLogin, ProfileForm, FormImage, CommentForm 


from django.conf import settings
import os


# Create your views here.
def index(request):
    images = Image.get_images()
    return render(request, 'home.html', {"images":images})

def signingup(request):
    if request.method == 'POST':
        form = FormSignUp(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_active = False
            user.save()
            current = get_current_site(request)
            subject = 'Activate your iNsTa'
            message = render_to_string('email/email.html', {
                'user': user, 
                'domain': current.domain, 
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
                })
            
            user.email_user(subject, message)
            return 'We have just sent you an email'
        else:
            form = FormSignUp()
        return render(request, 'registration/registration_form.html', {'form': form})

#code for activation below uses django-six library
def activate(request, uidb64, token):
  try:
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get()
  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None

  if user is not None and account_activation_token.check_token(user, token):
    user.is_active = True
    user.profile.email_confirmed = True
    user.save()
    login(request, user)
    return redirect(profile)
  else:
    return HttpResponse('The activation link is invalid')

def login(request):
    '''
    view function to display login form
    '''
    if request.method=='POST':
        form = FormLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['Username']
            password = form.cleaned_data['Password']
            
            user = authenticate(username,password)
            if user.is_active:
                login(request,user)
                return redirect(index)
            else:
                return HttpResponse("Your account is inactive")
            
    else:
        form=FormLogin()
    return render(request, 'registration/login.html',{"form":form})

@login_required(login_url='accounts/login')
def profile(request):
    '''
    function to create user profile
    '''
    current_user = request.user
    if request.method=="POST":
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile =form.save(commit=False)
            profile.user = current_user
            profile.save()
            return redirect(index)
    else:
        form = ProfileForm()
    return render(request, 'profile.html',{"form":form})

@login_required(login_url='accounts/login')
def profile_user(request, id):
    '''
    funcion to display user profile
    '''
    current_user = request.user
    profile = Profile.objects.filter(user_id=id).all()
    images = Image.objects.filter(profile_id=current_user.profile.id).all()
    return render(request, 'viewprofile.html', {"profile":profile, "images":images})

def uploadimage(request):
    '''
    view function to post images
    '''
    current_user = request.user
    if request.method=='POST':
        form = FormImage(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = current_user.profile
            image.save()
            return redirect(index)
    else:
        form = FormImage()
    return render(request, 'uploadimage.html',{"form":form})

def search(request):
    if 'user' in request.GET and request.GET['user']:
        search_user = request.GET.get('user')
        username_searched = Profile.search_by_profile(search_user)
        message = f'{search_user}'
        return render(request, 'search.html',{"users":username_searched, "message":message})


def logout_view(request):
    logout(request)

    return redirect(index)