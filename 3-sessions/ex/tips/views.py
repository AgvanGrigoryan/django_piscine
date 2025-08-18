from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from django.db.models import Count, Q
import random
import time
from .models import Tip
from .forms import TipCreatingForm
from .decorators import author_or_has_permission

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
    tips = Tip.objects.all().select_related('author').annotate(
        upvotes_count=Count('votes', filter=Q(votes__is_upvoted=True)),
        downvotes_count=Count('votes', filter=Q(votes__is_upvoted=False)),
    )
    if request.method == "POST" and request.user.is_authenticated:
        form = TipCreatingForm(request.POST)
        if form.is_valid():
            tip = form.save(commit=False)
            tip.author = request.user
            tip.save()
            return redirect('home_page')
        else:
            form.add_error(None, "Your Form is Invalid")
        return render(request, 'tips/home.html', {'form': form, 'tips': tips})
    form = TipCreatingForm()
    return render(request, 'tips/home.html', {'form': form, 'tips': tips})


# Tips Voting
@login_required
def upvote_view(request, pk):
    if request.method == 'GET':
        return redirect('home_page')
    try:
        tip = Tip.objects.get(pk=pk)
        tip.upvote(request.user)
        return redirect('home_page')
    except Tip.DoesNotExist:
        return HttpResponse(f"Tip by id {pk} not found", status=404)

@login_required
@author_or_has_permission('tips.can_downvote')
def downvote_view(request, pk):
    if request.method == 'GET':
        return redirect('home_page')
    try:
        tip = Tip.objects.get(pk=pk)
        tip.downvote(request.user)
        return redirect('home_page')
    except Tip.DoesNotExist:
        return HttpResponse(f"Tip by id {pk} not found", status=404)

@login_required
@author_or_has_permission('tips.delete_tip')
def delete_tip_view(request, pk):
    if request.method == 'GET':
        return redirect('home_page')
    try:
        tip = Tip.objects.get(pk=pk)
        tip.delete()
        return redirect('home_page')
    except Tip.DoesNotExist:
        return HttpResponse(f"Tip by id {pk} not found", status=404)
