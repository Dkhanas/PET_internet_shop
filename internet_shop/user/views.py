from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm

from utils.constants import LOGIN, LOGOUT, SIGN_UP, MAIN_PAGE

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect(LOGIN)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            user.save()
            login(request, user)
            return redirect(MAIN_PAGE)
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
                    return redirect(MAIN_PAGE)
        else:
            fm = AuthenticationForm()
        return render(request, 'login.html', {'form': fm})
    else:
        return redirect(MAIN_PAGE)


def user_logout(request):
    logout(request)
    return redirect(LOGIN)
