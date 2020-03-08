from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Image, Profile, Comment


from django.conf import settings
import os


# Create your views here.
@login_required(login_url='/accounts/register')
def index(request):
    images = Image.get_images()
    return render(request, 'home.html', {"images":images})