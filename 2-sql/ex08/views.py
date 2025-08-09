from django.shortcuts import render, HttpResponse, redirect
from django.db import connection, DatabaseError
from psycopg2 import sql
from django.urls import reverse
from urllib.parse import urlencode
import pathlib

BASE_DIR = pathlib.Path(__file__).parent

DATA_DIR = BASE_DIR / 'data'

PEOPLE_CSV = DATA_DIR / 'people.csv'
PLANETS_CSV = DATA_DIR / 'planets.csv'


PLANETS_TABLE_NAME='ex08_planets'

PLANETS_TABLE_SQL = sql.SQL("""
CREATE TABLE IF NOT EXISTS {} (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE,
    climate VARCHAR,
    diameter INTEGER,
    orbital_period INTEGER,
    population BIGINT,
	rotation_period INTEGER,
	surface_water REAL,
    terrain VARCHAR(128)
);
""").format(sql.Identifier(PLANETS_TABLE_NAME))

PEOPLE_TABLE_NAME='ex08_people'

PEOPLE_TABLE_SQL = sql.SQL("""
CREATE TABLE IF NOT EXISTS {} (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE,
    birth_year VARCHAR(32),
    gender VARCHAR(32),
    eye_color VARCHAR(32),
    hair_color VARCHAR(32),
	height INTEGER,
    mass REAL,
    homeworld VARCHAR(64) REFERENCES {}(name)
);
""").format(sql.Identifier(PEOPLE_TABLE_NAME), sql.Identifier(PLANETS_TABLE_NAME))

def init(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute(PLANETS_TABLE_SQL)
            cursor.execute(PEOPLE_TABLE_SQL)
        return HttpResponse("OK")
    except DatabaseError as e:
        return HttpResponse(f"An error occured: {e}", status=500)

def populate(request):
    with open(PLANETS_CSV, mode="r") as f:
        columns = tuple(f.readline().strip().split(','))
        with connection.cursor() as cursor:
            cursor.copy_from(f, PLANETS_TABLE_NAME, sep=',', columns=columns)

    with open(PEOPLE_CSV, mode="r") as f:
        columns = tuple(f.readline().strip().split(','))        
        with connection.cursor() as cursor:
            cursor.copy_from(f, PEOPLE_TABLE_NAME, sep=',', columns=columns)
            
    return HttpResponse("OK!")

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
    return render(request, 'ex06/display_movies.html', context)
