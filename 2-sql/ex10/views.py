from django.shortcuts import render
from .forms import SearchField
from django.db import DatabaseError
from django.db.models import Prefetch
from .models import People, Movies

def index(request):
    context = dict()
    form = SearchField(request.GET or None)

    context['is_first_request'] = True
    if request.GET:
        context['is_first_request'] = False
    try:
        if not context['is_first_request'] and form.is_valid():
            min_date = form.cleaned_data.get('min_release_date')
            max_date = form.cleaned_data.get('max_release_date')
            min_diameter = form.cleaned_data.get('min_planet_diameter')
            gender = form.cleaned_data.get('actor_gender')

            queryset = Movies.objects.all()
            if min_date:
                queryset = queryset.filter(release_date__gte=min_date)
            if max_date:
                queryset = queryset.filter(release_date__lte=max_date)
            
            queryset = People.objects.select_related('homeworld').prefetch_related(
                Prefetch('movies', queryset=queryset)
            )
            
            if min_diameter:
                queryset = queryset.filter(homeworld__diameter__gte=min_diameter)
            if gender:
                queryset = queryset.filter(gender=gender)
            
            queryset = [p for p in queryset if p.movies.exists()]

            context['result'] = queryset
            context['number_of_results'] = len(queryset)
    except DatabaseError as e:
        context['error_msg'] = str(e)

    context['form'] = form
    return render(request, 'ex10/search_info.html', context)

