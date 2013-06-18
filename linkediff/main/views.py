from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.user.is_authenticated():
        return redirect('home')
    if request.POST:
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('home')
                else:
                    raise Exception('Account disabled')
                    # Return a 'disabled account' error message
            else:
                return redirect('login')
    return render(request, 'login.html')        

def register(request):
    return render(request, 'register.html')

def logout(request):
    auth_logout(request)
    return redirect('home')