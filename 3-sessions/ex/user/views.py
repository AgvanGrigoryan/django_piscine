from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout

def register_view(request):
    # Redirect authenticated users to home page
    if request.user.is_authenticated:
        return redirect('home_page')
        
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home_page')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'user/registration.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home_page')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_page')
            else:
                form.add_error(None, "Invalid username or password")
                return render(request, 'user.login.html', {'form': form})
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'user/login.html', context)

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home_page')