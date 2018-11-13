from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from . import forms
from wallafood.models import Advert
import logging

# Create your views here.

def index(request):
    context = {}
    return render(request, "wallafood/login.html", context)

def register(request):
    form = forms.CreateUserForm(request.POST)

    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/wallafood/login")
    else:
        form = forms.CreateUserForm()

    return render(request, "wallafood/register.html", {'form': form})

def doLogin (request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User authenticated
            login(request, user)
            return redirect("/wallafood/advertisements")
        else:
            messages.error(request,'Incorrect user or password')
            return redirect("/wallafood/login")

@login_required(login_url='/wallafood/login')
def doLogout (request):
    logout(request)
    return redirect("/wallafood/login")

def forbidden(request):
    context = {}
    return render(request, "wallafood/forbidden.html", context)

def redirect_forbidden(request):
    if request.user.is_authenticated:
        return redirect("/wallafood/advertisements")
    else:
        return redirect("/wallafood/login")

@login_required(login_url='/wallafood/login')
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = forms.EditProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect("/wallafood/advertisements")
    else:
        form = forms.EditProfileForm(instance=user)
        
    return render(request, "wallafood/edit_profile.html", {'form': form,"user" : user})

@login_required(login_url='/wallafood/login')
def delete_user(request):
    username = request.GET.get('username')

    user = User.objects.get_by_natural_key(username)
    user.delete()
    return redirect("/wallafood/login")

@login_required(login_url='/wallafood/login')
def change_password(request):
    user = request.user

    if request.method == 'POST':
        form = forms.EditPasswordForm(data=request.POST, user=user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)            
            return redirect("/wallafood/advertisements")
    else:
        form = forms.EditPasswordForm(user=user)
    
    return render(request, "wallafood/change_password.html", {'form': form,"user" : user})

def advertisements(request):
    context = {}


    adverts = Advert.objects.all()
    #Advert.objects.get(name=adverts[0].name).delete()
    context = {
        'adverts': adverts
    } 

    return render(request, "wallafood/advertisements.html", context)

def addAdvert(request):
    form = forms.CreateAdvertForm(request.POST)

    if request.method == 'POST':
        form = forms.CreateAdvertForm(request.POST)
        logger = logging.getLogger(__name__)
        if form.is_valid():
            #logger.error(request.POST["name"])
            #logger.error(form['vendor'])
            advert = form.save(commit=False)
            advert.id_advert = 1
            advert.vendor = "el joji"
            advert.vote_average = 0
            advert.status = 'avialable'
            advert.save()
            return redirect("/wallafood/advertisements")
    else:
        form = forms.CreateAdvertForm()

    return render(request, "wallafood/add_advert.html", {'form': form})

@login_required(login_url='/wallafood/login')
def findAdvertisement(request):
    context = {}
    return render(request, "wallafood/advertisements.html", context)
"""
    if request.method == 'GET':
        text = request.GET['text_search']
        films = list(Movie.objects.raw('SELECT * FROM videoclub_movie WHERE title LIKE \'%'+text+'%\''))
        more_than_zero = True

        for movie in films:
            if movie.url_poster == 'None':
                movie.url_poster = 'https://unamo.com/assets/camaleon_cms/image-not-found-4a963b95bf081c3ea02923dceaeb3f8085e1a654fc54840aac61a57a60903fef.png'
            else:
                movie.url_poster = 'http://image.tmdb.org/t/p/w185/%s' % movie.url_poster

        context = {
            'more_than_zero': more_than_zero,
            'films': films,
        } 
"""