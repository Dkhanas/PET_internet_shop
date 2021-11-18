from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import SignUpForm
from PET_internet_shop.settings import *


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect(USER_APP_ROUTES['login'])


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            user.save()
            login(request, user)
            return redirect(USER_APP_ROUTES['main_page'])
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user:
                    login(request, user=user)
                    messages.success(request, 'Logged in successfully!')
                    return redirect(USER_APP_ROUTES['main_page'])
        else:
            fm = AuthenticationForm()
        return render(request, 'login.html', {'form': fm})
    else:
        return redirect(USER_APP_ROUTES['main_page'])


def user_logout(request):
    logout(request)
    return redirect(USER_APP_ROUTES['login'])
