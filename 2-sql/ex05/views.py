from django.shortcuts import render, HttpResponse, redirect
from django.db import DatabaseError
from .models import Movies
from .forms import MovieSelectForm
from django.urls import reverse
from urllib.parse import urlencode

MOVIES_TABLE_NAME='ex05_movies'

MOVIES_DATA = [
    {
        "episode_nb": 1,
        "title": "The Phantom Menace",
        "director": "George Lucas",
        "producer": "Rick McCallum",
        "release_date": "1999-05-19",
    },
    {
        "episode_nb": 2,
        "title": "Attack of the Clones",
        "director": "George Lucas",
        "producer": "Rick McCallum",
        "release_date": "2002-05-16",
    },
    {
        "episode_nb": 3,
        "title": "Revenge of the Sith",
        "director": "George Lucas",
        "producer": "Rick McCallum",
        "release_date": "2005-05-19",
    },
    {
        "episode_nb": 4,
        "title": "A New Hope",
        "director": "George Lucas",
        "producer": "Gary Kurtz, Rick McCallum",
        "release_date": "1977-05-25",
    },
    {
        "episode_nb": 5,
        "title": "The Empire Strikes Back",
        "director": "Irvin Kershner",
        "producer": "Gary Kurtz, Rick McCallum",
        "release_date": "1980-05-17",
    },
    {
        "episode_nb": 6,
        "title": "Return of the Jedi",
        "director": "Richard Marquand",
        "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
        "release_date": "1983-05-25",
    },
    {
        "episode_nb": 7,
        "title": "The Force Awakens",
        "director": "J. J. Abrams ",
        "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
        "release_date": "2015-12-11",
    },
]

def populate(request):
    try:
        for movie in MOVIES_DATA:
            m = Movies.objects.create(**movie)
        return HttpResponse("OK")
    except DatabaseError as e:
        return HttpResponse(f"An error occured: {e}", status=500)

def display(request):
    context = {}
    context['is_ok'] = True
    try:
        context['data'] = Movies.objects.all()
        if not context['data']:
            context['is_ok'] = False
            context['data'] = None
    except DatabaseError:
        context['is_ok'] = False
    context['error_msg'] = "No data available"
    return render(request, 'ex05/display_movies.html', context)

def remove(request):
    try:
        movies = Movies.objects.all()
        if not movies:
            return HttpResponse("No data available")
    except DatabaseError as e:
        return HttpResponse(f"An error occured: {e}", status=500)

    form = MovieSelectForm(Movies.objects.all(), request.POST or None)

    if request.method == "GET":
        msg = request.GET.get('msg')
        print(msg)
        return render(request, 'ex05/select_movie.html', {
            'form': form,
            'msg': msg
        })

    elif request.method == "POST":
        if form.is_valid():
            movie_title = form.cleaned_data['movie']
            try:
                result = movies.filter(title=movie_title).delete()
                if result[0] != 0:
                    msg = f"The Movie({movie_title}) deleted."
                else:
                    msg = f"The Movie({movie_title}) not found."
                url = reverse('delete_movie_05')
                query_string = urlencode({'msg': msg})
                return redirect(f"{url}?{query_string}")
            except DatabaseError as e:
                return HttpResponse(f"An error occured: {e}", status=500)
        else:
            return HttpResponse("The form you submitted is invalid!")
    return HttpResponse("Unsupported request method.", status=405)
