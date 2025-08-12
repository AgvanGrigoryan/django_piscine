from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import random
import time

def process_username(session):
    is_username_expired = False
    username = session.get('username', None)
    username_created_at = session.get('username_created', 0)

    if username_created_at != 0:
        if time.time() - username_created_at >= settings.USERNAME_EXPIRATION_SEC:
            is_username_expired = True
    
    if (
        username is None or
        username_created_at == 0 or
        is_username_expired
    ):
        session['username'] = random.choice(settings.AVAILABLE_USERNAMES)
        session['username_created'] = time.time()
    return session.get('username', "Unknown")

def get_username(request):
    username = process_username(request.session)
    return JsonResponse({'username': username})

def home_page(request):
    username = process_username(request.session)


    return render(request, 'tips/home.html', {'username': username})