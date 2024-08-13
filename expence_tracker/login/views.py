from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.messages import constants as messages
# Create your views here.

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login/login.html')
    
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # Check if the passwords match
        if password != confirm_password:
            return render(request, 'login/register.html', {'error': 'Passwords do not match'})

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'login/register.html', {'error': 'Username already exists'})

        
        # Create the new user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        # Log the user in and redirect to the home page
        login(request, user)
        # messages.SUCCESS(request, 'Registration successful!')
        return redirect('home')  # Assuming 'home' is the name of your home view URL pattern

    # For GET requests, render the registration form
    return render(request, 'login/register.html')


def Logout(request):
    logout(request)
    return redirect('login')