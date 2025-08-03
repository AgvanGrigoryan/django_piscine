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