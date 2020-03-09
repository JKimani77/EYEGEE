from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
# from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text

from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Image, Profile, Comment
from .forms import SignUpForm, LoginForm, ProfileForm, ImageForm, CommentForm 


from django.conf import settings
import os


# Create your views here.
@login_required(login_url='/accounts/register')
def index(request):
    images = Image.get_images()
    return render(request, 'home.html', {"images":images})

def signingup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_active = False
            user.save()
            current = get_current_site(request)
    #          to_email = form.cleaned_data.get('email')
    #         activation_email(user, current_site, to_email)
    #         return 'Check your email'
    # else:
            subject = 'Activate your iNsTa'
            # , 'token': account_activation_token.make_token(user) ---failed because of six library
            message = render_to_string('email/email.html', {'user': user, 'domain': current.domain, 'uid': urlsafe_base64_encode(force_bytes(user.pk))})
            
            user.email_user(subject, message)
            return redirect('home')
        else:
            form = SignUpForm()
            return render(request, 'signup.html', {'form': form})

#code for activation below uses django-six library
#has importation errors due to incompatibility of dependency(libraries) versions


# def activation(request, uidb64, token):
#   try:
#     uid = force_text(urlsafe_base64_decode(uidb64))
#     user = User.objects.get()
#   except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#     user = None

#   if user is not None and account_activation_token.check_token(user, token):
#     user.is_active = True
#     user.profile.email_confirmed = True
#     user.save()
#     login(request, user)
#     return render('request', 'emailactivate.html', {"uid":uid, "token":token})
#   else:
#     return HttpResponse('The activation link is invalid')

def login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['Username']
            password = form.cleaned_data['Password']
            
            user = authenticate(username,password)
            if user.is_active:
                login(request,user)
                return redirect(home)
            else:
                return HttpResponse("Your account is inactive")
            
    else:
        form=LoginForm()
    return render(request, 'registration/login.html',{"form":form})


@login_required(login_url='/accounts/register/')
def profile(request, id):
  profile = get_object_or_404(User, pk=id)
  images = profile.posts.all()
  return render(request, 'profile.html', {'profile':profile, 'images':images})


  def profile_user(request, id):
    current_user = request.user
    profile = Profile.objects.filter(user_id=id).all()
    images = Image.objects.filter(profile_id=current_user.profile.id).all()
    return render(request, 'viewprofile.html', {"profile":profile, "images":images})

def post_image(request):
    current_user = request.user
    if request.method=='POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = current_user.profile
            image.save()
            return redirect('home')
    else:
        form = ImageForm()
    return render(request, 'post_image.html',{"form":form})

# def specific_image(request, img_id):
#     image = Image.objects.get(pk=img_id)
    
#     return render(request,'single_image.html',{"image":image})



def logout(request):
    logout(request)

    return redirect(home)