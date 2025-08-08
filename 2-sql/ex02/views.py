from django.shortcuts import render, HttpResponse
from django.db import connection, DatabaseError
from psycopg2 import sql

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

MOVIES_TABLE_NAME='ex02_movies'

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
    query = sql.SQL(f"""
    INSERT INTO {{}} ("episode_nb", "title", "director", "producer", "release_date")
    VALUES (%s, %s, %s, %s, %s);
    """).format(sql.Identifier(MOVIES_TABLE_NAME))

    results = []
    for movie in MOVIES_DATA:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, [
                movie['episode_nb'],
                movie['title'],
                movie['director'],
                movie['producer'],
                movie['release_date']
            ])
            results.append(f"{movie['title']}: OK")
        except DatabaseError as e:
            results.append(f"{movie['title']}: Error: {e}")
    return HttpResponse("<br>".join(results))


def display(request):
    context = {}
    context['is_ok'] = True
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT * FROM {}").format(
                    sql.Identifier(MOVIES_TABLE_NAME)
                    )
                )
            context['data'] = cursor.fetchall()
            if context['data'] == []:
                context['is_ok'] = False
                context['data'] = None
    except DatabaseError:
        context['is_ok'] = False
    context['error_msg'] = "No data available"
    return render(request, 'ex02/display_movies.html', context)

