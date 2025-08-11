from django.shortcuts import render
from .models import People
from django.db import DatabaseError

DATA_IMPORT_CMD = "python manage.py import_ex09_data"
def display(request):
    context = {}
    context['is_ok'] = True
    try:
        context['data'] = People.objects.select_related('homeworld').filter(homeworld__climate__icontains="windy").order_by('name')
        if not context['data'].exists():
            context['is_ok'] = False
            context['data'] = None
    except DatabaseError:
        context['is_ok'] = False
    context['error_msg'] = f"No data available, please use the following command line before use: {DATA_IMPORT_CMD}"
    return render(request, 'ex09/display_peoples.html', context)
