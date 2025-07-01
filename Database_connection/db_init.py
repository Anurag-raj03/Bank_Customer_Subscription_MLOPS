import psycopg2
from psycopg2 import sql
import pandas as pd

# Database connection constants
DB_USER = "postgres"
DB_PASSWORD = "admin"
DB_PORT = "5432"
DB_HOST = "postgres"
TABLE_NAME = "subscribers"

# Define columns used for insertion and escaping
cols = ['age', 'job', 'marital', 'education', 'default', 'balance',
        'housing', 'loan', 'contact', 'day', 'month', 'duration',
        'campaign', 'pdays', 'previous', 'poutcome', 'y']

# Escape 'default' keyword for PostgreSQL safety
ESCAPED_COLUMNS = ', '.join([f'"{col}"' if col.lower() == 'default' else col for col in cols])


def create_database(DB_NAME):
    try:
        conn = psycopg2.connect(
            database='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}';")
        if not cur.fetchone():
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"[DB] Database '{DB_NAME}' created.")
        else:
            print(f"[DB] Database '{DB_NAME}' already exists.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[DB ERROR] Database creation failed: {e}")


def create_table(DB_NAME, TABLE_NAME):
    try:
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                age INT,
                job TEXT,
                marital TEXT,
                education TEXT,
                "default" TEXT,
                balance INT,
                housing TEXT,
                loan TEXT,
                contact TEXT,
                day INT,
                month TEXT,
                duration INT,
                campaign INT,
                pdays INT,
                previous INT,
                poutcome TEXT,
                y TEXT
            );
        """)
        conn.commit()
        print(f"[DB] Table '{TABLE_NAME}' created or already exists.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[DB ERROR] Table creation failed: {e}")


def insert_subscriber(DB_NAME, TABLE_NAME, data: dict):
    try:
        columns = list(data.keys())
        values = list(data.values())

        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()

        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(TABLE_NAME),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns))
        )
        cur.execute(insert_query, values)
        conn.commit()

        print(f"[DB] Record inserted into '{DB_NAME}.{TABLE_NAME}' successfully.")
        return True

    except Exception as e:
        print(f"[DB ERROR] Failed to insert record: {e}")
        return False

    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()


def clear_table(DB_NAME, TABLE_NAME):
    try:
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute(f"TRUNCATE TABLE {TABLE_NAME};")
        conn.commit()
        print(f"[DB] Table '{TABLE_NAME}' cleared.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[DB ERROR] Table clear failed: {e}")


def fetch_last_record(DB_NAME, TABLE_NAME):
    try:
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY ctid DESC LIMIT 1;")
        last_row = cur.fetchone()
        cur.close()
        conn.close()
        return last_row
    except Exception as e:
        print(f"[DB ERROR] Fetching last record failed: {e}")
        return None
