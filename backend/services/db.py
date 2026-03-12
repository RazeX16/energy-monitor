import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        database="energy_monitor",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )
    return conn