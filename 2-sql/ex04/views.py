from django.shortcuts import render, HttpResponse, redirect
from django.db import connection, DatabaseError
from psycopg2 import sql
from .forms import MovieSelectForm
from django.urls import reverse
from urllib.parse import urlencode

MOVIES_TABLE_SQL_TEMPLATE = sql.SQL("""
CREATE TABLE IF NOT EXISTS {} (
    episode_nb INTEGER PRIMARY KEY,
    title VARCHAR(64) NOT NULL UNIQUE,
    opening_crawl TEXT,
    director VARCHAR(32) NOT NULL,
    producer VARCHAR(128) NOT NULL,
    release_date DATE NOT NULL
);
""")

MOVIES_TABLE_NAME='ex04_movies'

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

def init(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                MOVIES_TABLE_SQL_TEMPLATE.format(
                    sql.Identifier(MOVIES_TABLE_NAME)
                )
            )
        return HttpResponse("OK")
    except DatabaseError as e:
        return HttpResponse(f"An error occured: {e}", status=500)

def populate(request):
    try:
        placeholders = ', '.join(['(%s, %s, %s, %s, %s)'] * len(MOVIES_DATA))
        query = f"""
        INSERT INTO {{}} ("episode_nb", "title", "director", "producer", "release_date")
        VALUES {placeholders};
        """
        formated_data = []
        for movie in MOVIES_DATA:
            formated_data.extend([
                movie['episode_nb'],
                movie['title'],
                movie['director'],
                movie['producer'],
                movie['release_date']
            ])

        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL(query).format(sql.Identifier(MOVIES_TABLE_NAME)),
                formated_data
            )
        return HttpResponse("OK")
    except DatabaseError as e:
        return HttpResponse(f"An error occured: {e}", status=500)

def get_all_movies(table_name: str):
    with connection.cursor() as cursor:
        cursor.execute(
            sql.SQL("SELECT * FROM {}").format(
                sql.Identifier(table_name)
                )
            )
        data = cursor.fetchall()
        if data == []:
            return ([], False)
        return (data, True)

def display(request):
    context = {}
    context['is_ok'] = True
    try:
        context['data'], context['is_ok'] = get_all_movies(MOVIES_TABLE_NAME)
    except DatabaseError:
        context['is_ok'] = False
    context['error_msg'] = "No data available"
    return render(request, 'ex04/display_movies.html', context)

def remove(request):
    try:
        movies, _ = get_all_movies(MOVIES_TABLE_NAME)
        if not movies:
            return HttpResponse("No data available")
    except DatabaseError as e:
        return HttpResponse(f"An error occured: {e}", status=500)

    choices = [(movie[1], movie[1]) for movie in movies]
    form = MovieSelectForm(choices, request.POST or None)

    if request.method == "GET":
        msg = request.GET.get('msg')
        return render(request, 'ex04/select_movie.html', {
            'form': form,
            'msg': msg
        })

    elif request.method == "POST":
        if form.is_valid():
            try:
                movie_title = form.cleaned_data['movie']
                with connection.cursor() as cursor:
                    cursor.execute(
                        sql.SQL("DELETE FROM {} WHERE title=%s").format(
                            sql.Identifier(MOVIES_TABLE_NAME)
                        ),
                        [movie_title]
                    )
                url = reverse('delete_movie')
                msg = f"The Movie({movie_title}) deleted."
                query_string = urlencode({'msg': msg})
                return redirect(f"{url}?{query_string}")
            except DatabaseError as e:
                return HttpResponse(f"An error occured: {e}", status=500)
        else:
            return HttpResponse("The form you submitted is invalid!")
    return HttpResponse("Unsupported request method.", status=405)
