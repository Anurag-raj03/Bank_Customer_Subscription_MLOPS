import psycopg2
import pandas as pd
from psycopg2 import sql

DB_USER="postgres"
DB_PASSWORD="admin"
DB_PORT="5432"
DB_HOST = "postgres"
TABLE_NAME="subscribers"

cols=['age', 'job', 'marital', 'education', 'default', 'balance',
           'housing', 'loan', 'contact', 'day', 'month', 'duration',
           'campaign', 'pdays', 'previous', 'poutcome', 'y']

ESCAPED_COLUMNS = ', '.join([f'"{col}"' if col.lower() == 'default' else col for col in cols])


def create_database(DB_NAME):
    try:
        conn=psycopg2.connect(database='postgres',user=DB_USER,password=DB_PASSWORD,host=DB_HOST,port=DB_PORT)
        conn.autocommit=True
        cur=conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}';")
        if not cur.fetchone():
            cur.execute(sql.SQL(f"CREATE DATABASE {DB_NAME}"))
            print(f"DataBase '{DB_NAME}' created.")
        else:
            print(f"Database '{DB_NAME} already exists.") 

        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Creation Error: {e}")

def create_table(DB_NAME,TABLE_NAME):
    try:
        conn=psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASSWORD,host=DB_HOST,port=DB_PORT)   
        cur=conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
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
        print(f"Table {TABLE_NAME} is ready")
        cur.close()
        conn.close()  
    except Exception as e:
        print(f"DB Creation Error: {e}")

def insert_subscriber(DB_NAME,TABLE_NAME,data:dict):
    try:
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        placeholders = ', '.join(['%s'] * len(cols))
        query = f"INSERT INTO {TABLE_NAME} ({ESCAPED_COLUMNS}) VALUES ({placeholders});"
        cur.execute(query, tuple(data[col] for col in cols))
        conn.commit()
        print(f"Record inserted into '{DB_NAME}.{TABLE_NAME}'")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Insertion Error: {e}")
    

           
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
        print(f"Table '{TABLE_NAME}' in database '{DB_NAME}' cleared.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Table Clear Error: {e}")

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
        print(f"Fetch Error: {e}")
        return None
