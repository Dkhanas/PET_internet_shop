from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post
from .forms import SignUpForm


def post_list(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return render(request, 'blog/post_list.html', {'posts': posts})
    else:
        return redirect('/login/')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            user.save()
            raw_password = form.cleaned_data.get('password1')
            login(request, user)
            # redirect user to home page
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})


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
                    messages.success(request, 'Logged in successfully!!!')
                    return redirect('/')
        else:
            fm = AuthenticationForm()
        return render(request, 'blog/login.html', {'form': fm})
    else:
        return redirect('/')


def user_logout(request):
    logout(request)
    return redirect('/login/')
