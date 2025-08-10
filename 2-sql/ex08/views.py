from django.shortcuts import render, HttpResponse, redirect
from django.db import connection, DatabaseError
from psycopg2 import sql
from django.urls import reverse
from urllib.parse import urlencode
import pathlib
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from io import StringIO
import csv

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
    homeworld VARCHAR(64) REFERENCES {}(name) ON DELETE CASCADE
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

def insert_from_file(filename, table, sep=",") -> list[str]:
    results = list()
    with open(filename, mode="r") as f:
        collection_name = filename.name
        reader = csv.DictReader(f, delimiter=sep)
        columns = list(map(str.strip, reader.fieldnames))
        for row in reader:
            row = {k.strip() if isinstance(k, str) else k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
            try:
                line_data = sep.join(row[col] for col in columns)
                line_id = row.get('id', row.get('name', 'Unknown'))
            except KeyError as e:
                results.append(f"{filename.name} Error: missing column {e}")
                continue
            try:
                with connection.cursor() as cursor:
                    cursor.copy_from(
                        StringIO(line_data + "\n"),
                        table, sep=sep,
                        columns=columns)
                results.append(f"{collection_name}: {line_id}: OK")
            except (DatabaseError, UniqueViolation, ForeignKeyViolation) as e:
                results.append(f"{collection_name}: {line_id}: Error: {e}")
    return results

def populate(request):
    # COPY FROM PLANETS_CSV
    logs = insert_from_file(PLANETS_CSV, PLANETS_TABLE_NAME)
    result = f"""
    <h2>{PLANETS_TABLE_NAME}</h2>
    <br>
    {"<br><br>".join(logs)}
    <hr>
    """
    # COPY FROM PEOPLE_CSV
    logs = insert_from_file(PEOPLE_CSV, PEOPLE_TABLE_NAME)
    result += f"""
    <h2>{PEOPLE_TABLE_NAME}</h2>
    <br>
    {"<br><br>".join(logs)}
    """
    return HttpResponse(result)

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
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("""
                    SELECT t1.name, t1.homeworld, t2.climate 
                    FROM {} as t1 
                    JOIN {} as t2 ON t1.homeworld = t2.name
                    WHERE t2.climate ILIKE %s
                    ORDER BY t1.name ASC
                """).format(
                    sql.Identifier(PEOPLE_TABLE_NAME),
                    sql.Identifier(PLANETS_TABLE_NAME)
                ),
                ['%windy%']
            )
            data = cursor.fetchall()
            if data == []:
                context['is_ok'] = False
                context['data'] = None
            else:
                context['data'] = data
    except DatabaseError:
        context['is_ok'] = False
    context['error_msg'] = "No data available"
    return render(request, 'ex08/display_peoples.html', context)
