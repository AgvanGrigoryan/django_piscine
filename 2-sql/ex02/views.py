from django.shortcuts import render, HttpResponse
from django.db import connection, DatabaseError
from psycopg2 import sql
from sql.templates import MOVIES_TABLE_SQL_TEMPLATE

def init(request):
    pass