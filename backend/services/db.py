import psycopg2
from services.auth import hash_password


def get_db_connection():
    conn = psycopg2.connect(
        database="energy-monitor",
        user="postgres",
        password="Ajdil@29",
        host="localhost",
        port="5432"
    )
    return conn


users = {
    "admin": {
        "username": "admin",
        "password": hash_password("1234"),
        "role": "admin"
    }
}