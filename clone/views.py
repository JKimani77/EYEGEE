from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text

from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Image, Profile, Comment
from .forms import SignUpForm


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
            subject = 'Activate your iNsTa'
            message = render_to_string('email/email.html', {'user': user, 'domain': current.domain, 'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation_token.make_token(user),})
            
            user.email_user(subject, message)
            return redirect('home')
        else:
            form = SignUpForm()
            return render(request, 'signup.html', {'form': form})


def activation(request, uidb64, token):
  try:
    user = User.objects.get()
  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None

  if user is not None and account_activation_token.check_token(user, token):
    user.is_active = True
    user.profile.email_confirmed = True
    user.save()
    login(request, user)
    return redirect('home')
  else:
    return render(request, 'accountinvalid.html')


@login_required(login_url='/accounts/register/')
def profile(request, id):
  profile = get_object_or_404(User, pk=id)
  images = profile.posts.all()
  return render(request, 'actual/profile.html', {'profile':profile, 'images':images})