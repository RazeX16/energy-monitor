import psycopg2
from backend.services.auth_service import hash_password


def get_db_connection():
    conn = psycopg2.connect(
        database="energy_monitor",
        user="postgres",
        password="password",
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