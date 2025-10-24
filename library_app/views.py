from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User

def home(request):
    return render(request, 'library_app/home.html')  # homepage

def signup_user(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        account_name = request.POST['account_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('signup')

        if User.objects.filter(account_name=account_name).exists():
            messages.error(request, 'Username already taken!')
            return redirect('signup')

        user = User.objects.create(
            full_name=full_name,
            email=email,
            account_name=account_name,
            password=password
        )
        messages.success(request, 'Account created. Please log in.')
        return redirect('login')

    return render(request, 'library_app/signup.html')

def login_user(request):
    if request.method == 'POST':
        account_name = request.POST['account_name']
        password = request.POST['password']

        # improve this logic later with password hashing
        user = User.objects.filter(account_name=account_name, password=password).first()

        if user:
            request.session['user_id'] = user.id  # save session
            messages.success(request, f'Welcome {user.account_name}')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'library_app/login.html')

def logout_user(request):
    request.session.flush()  # Clear session
    messages.success(request, 'You have been logged out.')
    return redirect('login')
from django.shortcuts import render

# Create your views here.
