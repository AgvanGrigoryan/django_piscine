from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.conf import settings
import random
import time
from .models import Tip
from .forms import TipCreatingForm

def get_display_username(request):
    if request.user.is_authenticated:
        return request.user.username

    username = request.session.get('username', None)
    created_at = request.session.get('username_created_at', 0)

    is_expired = created_at == 0 or time.time() - created_at >= settings.USERNAME_EXPIRATION_SEC
    if username is None or is_expired:
        username = random.choice(settings.AVAILABLE_USERNAMES)
        request.session['username'] = username
        request.session['username_created_at'] = time.time()

    return username

def username_api(request):
    return JsonResponse({'username': get_display_username(request)})

def home_page(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = TipCreatingForm(request.POST)
        if form.is_valid():
            tip = form.save(commit=False)
            tip.author = request.user
            tip.save()
            return redirect('home_page')
        else:
            form.add_error("Your Form is Invalid")
        return render(request, 'tips/home.html', {'form': form})
        return HttpResponse("OLA")
    form = TipCreatingForm()
    tips = Tip.objects.all().select_related('author')
    return render(request, 'tips/home.html', {'form': form, 'tips': tips})