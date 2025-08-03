from django.shortcuts import render, HttpResponse
from django.db import connection, DatabaseError
from psycopg2 import sql
from sql.templates import MOVIES_TABLE_SQL_TEMPLATE

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
                MOVIES_TABLE_SQL_TEMPLATE.format(sql.Identifier(MOVIES_TABLE_NAME))
            )
        return HttpResponse("OK")
    except DatabaseError as e:
        return HttpResponse(f"An error occured: {e}", status=500)

def populate(request):
    try:
        query = f"""
        INSERT INTO {{}} ("episode_nb", "title", "director", "producer", "release_date")
        VALUES {', '.join('(%s, %s, %s, %s, %s)' for _ in range(len(MOVIES_DATA)))};
        """
        formated_data = []
        for movie in MOVIES_DATA:
            ordered_movie_fields = [movie['episode_nb'],movie['title'], movie['director'], movie['producer'], movie['release_date']]
            formated_data.extend(ordered_movie_fields)
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL(query).format(sql.Identifier(MOVIES_TABLE_NAME)),
                formated_data
            )
        return HttpResponse("OK")
    except DatabaseError as e:
        return HttpResponse(f"An error occured: {e}", status=500)

