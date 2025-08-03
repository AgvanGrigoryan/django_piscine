from django.shortcuts import render, HttpResponse
from django.db import connection, DatabaseError
from sql.ex00 import CREATE_MOVIES_TABLE

def init(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
        return HttpResponse("OK")
    except DatabaseError as e:
        return HttpResponse(f"An error occured: {e}", status=500)