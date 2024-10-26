import sqlite3, psycopg2
from decouple import config
from psycopg2 import sql

# Connect to the SQLite database
sqlite_conn = sqlite3.connect('keywords.db')

# Connect to the PostgreSQL database
pg_conn = psycopg2.connect(
    dbname=config('DATABASE_NAME'),
    user=config('DATABASE_USER'),
    password=config('DATABASE_PASSWORD'),
    host=config('DATABASE_HOST'),
    port=config('DATABASE_PORT')
)
pg_cursor = pg_conn.cursor()

pg_cursor.execute('''
    CREATE TABLE IF NOT EXISTS modules.keywords (
        id SERIAL PRIMARY KEY,
        module_code TEXT NOT NULL,
        big_topic TEXT,
        topic_content TEXT,
        keywords TEXT,
        examinable BOOLEAN
    )
''')
pg_conn.commit()

# Get the list of tables in the SQLite database
sqlite_cursor = sqlite_conn.cursor()
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = sqlite_cursor.fetchall()

# Iterate over each table and insert the data into the PostgreSQL table
for table in tables:
    table_name = table[0]
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()
    for row in rows:
        pg_cursor.execute(
            sql.SQL("INSERT INTO modules.keywords (module_code, big_topic, topic_content, keywords, examinable) VALUES (%s, %s, %s, %s, %s)"),
            [table_name, row[1], row[2], row[3], row[4] == 1]
        )

# Commit the changes and close the connections
pg_conn.commit()
sqlite_conn.close()
pg_conn.close()