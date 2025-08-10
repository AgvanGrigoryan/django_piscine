from django.shortcuts import render
from .models import People
from django.db import DatabaseError

def display(request):
    context = {}
    context['is_ok'] = True
    try:
        context['data'] = People.objects.filter(homeworld__climate__icontains="windy").order_by('name')
        if not context['data'].exists():
            context['is_ok'] = False
            context['data'] = None
    except DatabaseError:
        context['is_ok'] = False
    context['error_msg'] = "No data available, please use the following command line before use:"
    return render(request, 'ex07/display_movies.html', context)

def populate(request):
    pass
