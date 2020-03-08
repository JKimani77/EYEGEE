from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
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

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_active = False
            user.save()
            current = get_current_site(request)
            subject = 'Activate your iNsTa'
            message = render_to_string('email/email.html', {'user': user, 'domain': current.domain,})
            
            user.email_user(subject, message)
            return redirect('home')
        else:
            form = SignUpForm()
            return render(request, 'signup.html', {'form': form})

