from django.shortcuts import render

def register(request):
    return render(request, 'user/registration.html')

def login(request):
    return render(request, 'user/login.html')
