import re

from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.views.generic import TemplateView

from utils.constants import LOGIN, SIGN_UP, MAIN_PAGE, SIGN_UP_TEMPLATE, LOGIN_TEMPLATE


class SignUpView(TemplateView):
    form_class = SignUpForm
    template_name = SIGN_UP_TEMPLATE

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            if re.search('[0-9a-z]+@[a-z.]+', username):
                user.email = username
            else:
                user.phone = username
            user.save()
            login(request, user)
            return redirect(MAIN_PAGE)
        return render(request, self.template_name, {'form': form})


class LoginView(TemplateView):
    form_class = LoginForm
    template_name = LOGIN_TEMPLATE

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user=user)
                return redirect(MAIN_PAGE)
            else:
                return render(request, self.template_name, {'form': self.form_class()})
        return render(request, self.template_name, {'form': form})


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect(LOGIN)


def user_logout(request):
    logout(request)
    return redirect(LOGIN)
