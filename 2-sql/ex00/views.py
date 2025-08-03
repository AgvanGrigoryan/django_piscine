from django.shortcuts import render, HttpResponse
from django.db import connection, DatabaseError
from psycopg2 import sql
from sql.templates import MOVIES_TABLE_SQL_TEMPLATE

def init(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                MOVIES_TABLE_SQL_TEMPLATE.format(sql.Identifier('ex00_movies'))
            )
        return HttpResponse("OK")
    except DatabaseError as e:
        return HttpResponse(f"An error occured: {e}", status=500)